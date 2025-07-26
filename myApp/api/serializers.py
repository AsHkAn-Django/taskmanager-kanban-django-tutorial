from myApp.models import Task
from rest_framework import serializers
from users.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Override the serializer for telling it to use emial for authentication and creating token
    because our custom user model has only email and not username but the default login for JWT
    is base on username.
    """
    username_field = 'email'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'is_complete']
        read_only_fields = ['user']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "full_name", "is_staff", "is_superuser"]
