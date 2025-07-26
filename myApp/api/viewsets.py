from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView

from myApp.models import Task
from .serializers import CustomUserSerializer, TaskSerializer, MyTokenObtainPairSerializer
from users.models import CustomUser
from .permissions import IsAuthenticatedAndIsAuthor


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedAndIsAuthor]

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

    @action(detail=True, methods=['get'])
    def move_up(self, request, pk=None):
        """Move the task one step higher in the list."""
        task = self.get_object()
        task_order = task.order
        tasks_above = Task.objects.filter(user=task.user, order__lt=task_order).order_by('order')
        if not tasks_above:
            return Response({"error": f"'{task.name}' is already on top of the list."}, status=status.HTTP_400_BAD_REQUEST)

        chosen_task = tasks_above.last()
        task.order, chosen_task.order = chosen_task.order, task.order
        task.save()
        chosen_task.save()
        return Response({"success": f"'{task.name}' went one step up."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def move_down(self, request, pk=None):
        """Move the task one step higher in the list."""
        task = self.get_object()
        task_order = task.order
        tasks_under = Task.objects.filter(user=task.user, order__gt=task_order).order_by('order')
        if not tasks_under:
            return Response({"error": f"'{task.name}' is already at the bottom of the list."}, status=status.HTTP_400_BAD_REQUEST)

        chosen_task = tasks_under.first()
        task.order, chosen_task.order = chosen_task.order, task.order
        task.save()
        chosen_task.save()
        return Response({"success": f"'{task.name}' went one step down."}, status=status.HTTP_200_OK)

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]



class MyTokenObtainPairView(TokenObtainPairView):
    """
    Use the custom serializer which uses email as login not username.
    """
    serializer_class = MyTokenObtainPairSerializer