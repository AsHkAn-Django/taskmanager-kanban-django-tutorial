from rest_framework import viewsets
from myApp.models import Task
from . import serializers


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    