from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from django.conf import settings
import os

from .models import GoogleCredentials

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from .forms import CalendarEventForm
from .models import CalendarEvent

@login_required
def create_event(request):
    if request.method == 'POST':
        form = CalendarEventForm(request.POST)
        if form.is_valid():
            # Save local event
            event = form.save(commit=False)
            event.user = request.user
            event.save()

            # Create Google Calendar event
            try:
                credentials = get_google_credentials(request.user)
                service = build('calendar', 'v3', credentials=credentials)

                event = {
                    'summary': form.cleaned_data['title'],
                    'description': form.cleaned_data['description'],
                    'start': {
                        'date': form.cleaned_data['date'].isoformat(),
                        'timeZone': 'UTC',
                    },
                    'end': {
                        'date': form.cleaned_data['date'].isoformat(),
                        'timeZone': 'UTC',
                    },
                }

                created_event = service.events().insert(calendarId='primary', body=event).execute()
                
                # Optionally, you could store the Google Calendar event ID
                return redirect('chat:event_list')
            except Exception as e:
                # Handle API errors
                form.add_error(None, f"Google Calendar error: {str(e)}")
    else:
        form = CalendarEventForm()

    return render(request, 'chat/create_event.html', {'form': form})

@login_required
def event_list(request):
    events = CalendarEvent.objects.filter(user=request.user).order_by('-date')
    return render(request, 'chat/event_list.html', {'events': events})

def google_auth_start(request):
    flow = get_google_auth_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent',
        include_granted_scopes='true'
    )
    request.session['google_auth_state'] = state
    return redirect(authorization_url)

def google_auth_callback(request):
    state = request.session.get('google_auth_state')
    flow = get_google_auth_flow()
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials
    
    # Store credentials (implement secure storage method)
    save_google_credentials(request.user, credentials)

    return redirect('chat:create_event')

def get_google_auth_flow():
    return Flow.from_client_config(
        client_config=settings.GOOGLE_CALENDAR_CREDENTIALS,
        scopes=settings.GOOGLE_CALENDAR_SCOPES,
        redirect_uri=settings.GOOGLE_CALENDAR_CREDENTIALS['web']['redirect_uris'][0]
    )

def save_google_credentials(user, credentials):
    google_creds, _ = GoogleCredentials.objects.get_or_create(user=user)
    google_creds.token = credentials.token
    google_creds.token_uri = credentials.token_uri
    google_creds.client_id = credentials.client_id
    google_creds.client_secret = credentials.client_secret
    google_creds.scopes = ",".join(credentials.scopes)

    # Store refresh_token only if available
    if credentials.refresh_token:
        google_creds.refresh_token = credentials.refresh_token

    google_creds.save()

def get_google_credentials(user):
    try:
        google_creds = GoogleCredentials.objects.get(user=user)
        return Credentials(
            token=google_creds.token,
            refresh_token=google_creds.refresh_token,
            token_uri=google_creds.token_uri,
            client_id=google_creds.client_id,
            client_secret=google_creds.client_secret,
            scopes=google_creds.scopes.split(","),
        )
    except GoogleCredentials.DoesNotExist:
        return None
