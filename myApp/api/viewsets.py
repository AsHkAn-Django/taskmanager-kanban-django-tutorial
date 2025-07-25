from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from myApp.models import Task
from . import serializers
from users.models import CustomUser


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def reorder(self, request):
        """Swap the order of two tasks by their IDs."""
        pk1 = request.data.get('pk1')
        pk2 = request.data.get('pk2')

        if not pk1 or not pk2:
            return Response({'error': 'Both pk1 and pk2 are required.'}, status=status.HTTP_400_BAD_REQUEST)

        task1 = get_object_or_404(Task, pk=pk1, user=request.user)
        task2 = get_object_or_404(Task, pk=pk2, user=request.user)

        task1.order, task2.order = task2.order, task1.order
        task1.save()
        task2.save()
        return Response({"message": f"'{task1.name}' has been swapped with '{task2.name}'!"}, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = serializers.CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]