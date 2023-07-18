from rest_framework.permissions import BasePermission


class DirectUpdatePermission(BasePermission):
    """
    Checks if user is owner the product or an admin or has permission to direct update all
    """
    message = "You are not allowed to do this"

    def has_permission(self, request, view):
        instance = view.get_object()
        return (instance.user == request.user and request.user.groups.filter(name="Can Direct Update").exists()) or \
               request.user.groups.filter(name="Admin").exists() or \
               request.user.groups.filter(name="Can Direct Update All").exists()


class IsProductOwnerOrAdmin(BasePermission):
    """
    Checks if user is owner the product or an admin
    """
    message = "You are not allowed to do this"

    def has_permission(self, request, view):
        instance = view.get_object()
        return instance.user == request.user or request.user.groups.filter(name="Admin").exists()


class IsProductOwner(BasePermission):
    """
    Checks if user is owner the product
    """
    message = "You are not allowed to do this"

    def has_permission(self, request, view):
        instance = view.get_object()
        return instance.user == request.user


class IsProductVariantOwner(BasePermission):
    """
    Checks if user is owner the product
    """
    message = "You are not allowed to do this"

    def has_permission(self, request, view):
        instance = view.get_object()
        return instance.product.user == request.user
