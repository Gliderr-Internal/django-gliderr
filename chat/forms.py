from django import forms
from .models import Event

class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['summary', 'description', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }