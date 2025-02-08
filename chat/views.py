from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from sim.views import get_calendar_service
from datetime import datetime, timedelta

from .models import Event

@login_required
def create_event(request):
    if request.method == 'POST':
        service = get_calendar_service(request.user)

        start_time = datetime.fromisoformat(request.POST.get('start_time')).isoformat()
        end_time = datetime.fromisoformat(request.POST.get('end_time')).isoformat()
        
        event = {
            'summary': request.POST.get('summary'),
            'description': request.POST.get('description'),
            'start': {
                'dateTime': start_time,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'UTC',
            }
        }
        
        try:
            event = service.events().insert(calendarId='primary', body=event).execute()
            Event.objects.create(
                user=request.user,
                google_event_id=event['id'],
                summary=event['summary'],
                description=event['description'],
                start_time=request.POST.get('start_time'),
                end_time=request.POST.get('end_time')
            )
            return JsonResponse({'success': True, 'eventId': event['id']})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return render(request, 'chat/create_event.html')

@login_required
def event_list(request):
    service = get_calendar_service(request.user)
    
    # Get events for next 7 days
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    
    try:
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        
        # Process events to ensure consistent datetime format
        processed_events = []
        for event in events:
            processed_event = {
                'summary': event.get('summary', 'No Title'),
                'description': event.get('description', ''),
                'start_time': event['start'].get('dateTime', event['start'].get('date', '')),
                'end_time': event['end'].get('dateTime', event['end'].get('date', '')),
                'id': event['id']
            }
            processed_events.append(processed_event)
            
        return render(request, 'chat/event_list.html', {'events': processed_events})
    except Exception as e:
        return render(request, 'chat/event_list.html', {'error': str(e)})
    