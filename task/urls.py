from django.urls import path
from . import views

app_name = 'task'

urlpatterns = [
    path('', views.task_view, name='task_view'),
    path('view/', views.view_task, name='view_task'),
    path('delete/', views.delete_task, name='delete_task'),
]