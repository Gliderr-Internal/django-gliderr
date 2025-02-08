import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from .models import User

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.urls import reverse
from datetime import datetime, timezone

def get_google_flow(request):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=settings.GOOGLE_OAUTH_SCOPES,
        redirect_uri=request.build_absolute_uri(reverse('sim:auth_receiver'))
    )
    return flow


@csrf_exempt
def sign_in(request):
    if request.user.is_authenticated:
        return redirect("chat:create_event")
    
    flow = get_google_flow(request)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    
    request.session['state'] = state
    return redirect(authorization_url)


@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    flow = get_google_flow(request)
    flow.fetch_token(
        authorization_response=request.build_absolute_uri(),
        state=request.session['state']
    )
    
    credentials = flow.credentials
    token_info = id_token.verify_oauth2_token(
        credentials.id_token,
        requests.Request(),
        settings.GOOGLE_OAUTH_CLIENT_ID
    )
    
    user, created = User.objects.get_or_create(
        email=token_info['email'],
        defaults={
            'username': token_info['email'],
            'google_id': token_info['sub'],
            'first_name': token_info.get('given_name', ''),
            'last_name': token_info.get('family_name', ''),
        }
    )
    
    user.access_token = credentials.token
    user.refresh_token = credentials.refresh_token
    user.token_expiry = datetime.fromtimestamp(credentials.expiry.timestamp(), tz=timezone.utc)
    user.save()
    
    login(request, user)
    return redirect('chat:create_event')

def get_calendar_service(user):
    credentials = Credentials(
        token=user.access_token,
        refresh_token=user.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=settings.GOOGLE_OAUTH_SCOPES
    )
    
    return build('calendar', 'v3', credentials=credentials)


def sign_out(request):
    logout(request)
    return redirect("sim:sign_in")
