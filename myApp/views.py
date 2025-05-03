from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView
from .models import Task
from .forms import TaskForm
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_protect  


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



@csrf_protect
def reorder_items(request):
    """
    Accepts a JSON POST request with a list of item IDs in new order.
    Updates each item's 'order' field to reflect the new order.
    """
    try:
        # Parse JSON request body into Python dictionary
        data = json.loads(request.body)

        # Extract the 'order' list from the data
        order = data.get('order', [])

        # Update each item in the database
        for index, task_id in enumerate(order):
            task = Task.objects.get(id=task_id)
            task.order = index
            task.save()

        # Respond with success
        return JsonResponse({'status': 'success'})
    except Exception as e:
        # If something goes wrong, respond with an error
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)