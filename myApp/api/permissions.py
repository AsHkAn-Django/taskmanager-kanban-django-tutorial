from rest_framework import permissions



class IsAuthenticatedAndIsAuthor(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to access it,
    and only if they are authenticated.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user