from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView
from .models import Task
from .forms import TaskForm
from django.shortcuts import get_object_or_404, redirect


class IndexView(TemplateView):
    template_name = 'myApp/index.html'


class AddTaskView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'myApp/task_new.html'
    success_url = reverse_lazy('task_list')


class TaskListView(ListView):
    model = Task
    template_name = 'myApp/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.order_by('is_complete')


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'myApp/task_edit.html'
    success_url = reverse_lazy('task_list')


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'myApp/task_delete.html'
    success_url = reverse_lazy('task_list')


def task_complete(request, pk):
    """Toggle between completed and uncompleted a task."""
    task = get_object_or_404(Task, id=pk)
    task.is_complete = not task.is_complete
    task.save()
    return redirect('task_list')
