from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sim.urls')),
    path('accounts/', include('sim.urls')),
    path('chat/', include('chat.urls')),
    path('task/', include('task.urls')),
]
