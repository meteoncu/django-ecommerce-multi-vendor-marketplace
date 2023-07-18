from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Checks if user is an admin
    """
    message = "You are not allowed to do this"

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Admin").exists()


class IsSelf(BasePermission):
    """
    Checks if the user is him self
    """
    message = "You are not allowed to do this"

    def has_permission(self, request, view):
        instance = view.get_object()
        return instance == request.user

