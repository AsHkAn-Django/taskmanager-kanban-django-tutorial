from . import viewsets
from rest_framework.routers import DefaultRouter
from django.urls import path, include


router = DefaultRouter()
router.register(r'quotes', viewsets.TaskViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls)),
]