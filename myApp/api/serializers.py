from myApp.models import Task
from rest_framework import serializers
from users.models import CustomUser


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'is_complete']
        read_only_fields = ['user']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "full_name", "is_staff", "is_superuser"]
