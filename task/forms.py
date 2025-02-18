from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['q1', 'q2', 'q3', 'q4', 'q5']
        labels = {
            'q1': 'Question 1',
            'q2': 'Question 2',
            'q3': 'Question 3',
            'q4': 'Question 4',
            'q5': 'Question 5',
        }
        widgets = {
            'q1': forms.Textarea(attrs={'rows': 3}),
            'q2': forms.Textarea(attrs={'rows': 3}),
            'q3': forms.Textarea(attrs={'rows': 3}),
            'q4': forms.Textarea(attrs={'rows': 3}),
            'q5': forms.Textarea(attrs={'rows': 3}),
        }