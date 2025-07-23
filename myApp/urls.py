from django.urls import path
from .views import IndexView, AddTaskView, TaskListView, TaskUpdateView, TaskDeleteView, task_complete, reorder_items

urlpatterns = [
    path('task/<int:pk>/task_complete', task_complete, name='task_complete'),
    path('task/<int:pk>/delete', TaskDeleteView.as_view(), name='task_delete'),
    path('task/<int:pk>/edit', TaskUpdateView.as_view(), name='task_edit'),
    path('task_list/', TaskListView.as_view(), name='task_list'),
    path('reorder/', reorder_items, name='reorder-items'),        
    path('task_new/', AddTaskView.as_view(), name='task_new'),
    path('', IndexView.as_view(), name='home'),
]
