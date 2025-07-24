from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm


class SignUpView(generic.CreateView):
    model = get_user_model
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = "users/signup.html"
