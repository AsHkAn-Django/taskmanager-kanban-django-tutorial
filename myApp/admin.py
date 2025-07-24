from django.contrib import admin
from .models import Task
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import CustomUser
from django.forms import ModelForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ("email", "full_name")


class UserChangeForm(ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ("email", "full_name", "password", "is_active", "is_staff", "is_superuser")


class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = CustomUser
    list_display = ("email", "full_name", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name",)}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "password1", "password2"),
        }),
    )
    search_fields = ("email",)
    ordering = ("email",)



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Task)
