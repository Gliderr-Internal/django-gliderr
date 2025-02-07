from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.create_event, name='create_event'),
    path('events/', views.event_list, name='event_list'),
    path('google/auth/', views.google_auth_start, name='google_auth_start'),
    path('google/callback/', views.google_auth_callback, name='google_auth_callback'),
]