from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('create-event/', views.create_event, name='create_event'),
    path('list-events/', views.event_list, name='event_list'),
]