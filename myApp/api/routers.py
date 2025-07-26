from . import viewsets
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView


router = DefaultRouter()
router.register(r'tasks', viewsets.TaskViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls)),
    path('users/', viewsets.UserListView.as_view()),
    path('token/', viewsets.MyTokenObtainPairView.as_view(), name='token_obtain_pair'), # using the custom tokenobtainpair view to get email not username
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]