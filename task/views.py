from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

@login_required
def task_view(request):
    # Check if user already has a task
    try:
        task = Task.objects.get(user=request.user)
        return redirect('task:view_task')
    except Task.DoesNotExist:
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                return redirect('task:view_task')
        else:
            form = TaskForm()
        
        return render(request, 'task/create_task.html', {'form': form})

@login_required
def view_task(request):
    try:
        task = Task.objects.get(user=request.user)
        return render(request, 'task/view_task.html', {'task': task})
    except Task.DoesNotExist:
        return redirect('task:task_view')

@login_required
def delete_task(request):
    if request.method == 'POST':
        Task.objects.filter(user=request.user).delete()
    return redirect('task:task_view')