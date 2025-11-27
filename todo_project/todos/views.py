from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Todo
from .forms import TodoForm


def home(request):
    """Display all TODOs"""
    todos = Todo.objects.all()
    context = {
        'todos': todos,
        'now': timezone.now()
    }
    return render(request, 'home.html', context)


def create_todo(request):
    """Create a new TODO"""
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TodoForm()
    
    return render(request, 'todo_form.html', {'form': form, 'action': 'Create'})


def edit_todo(request, todo_id):
    """Edit an existing TODO"""
    todo = get_object_or_404(Todo, id=todo_id)
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TodoForm(instance=todo)
    
    return render(request, 'todo_form.html', {'form': form, 'action': 'Edit', 'todo': todo})


def delete_todo(request, todo_id):
    """Delete a TODO"""
    todo = get_object_or_404(Todo, id=todo_id)
    
    if request.method == 'POST':
        todo.delete()
        return redirect('home')
    
    return render(request, 'todo_confirm_delete.html', {'todo': todo})


def mark_completed(request, todo_id):
    """Mark a TODO as completed"""
    todo = get_object_or_404(Todo, id=todo_id)
    
    if request.method == 'POST':
        todo.completed = True
        todo.save()
    
    return redirect('home')
