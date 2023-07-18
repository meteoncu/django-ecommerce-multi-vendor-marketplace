from rest_framework.permissions import BasePermission


class IsLineItemOwner(BasePermission):
    """
    Checks if user is owner the order
    """
    message = "You are not allowed to do this"

    def has_permission(self, request, view):
        instance = view.get_object()
        return instance.order.user == request.user


class IsLineItemNotPurchased(BasePermission):
    """
    Checks if line item is not purchased
    """
    message = "Already purchased"

    def has_permission(self, request, view):
        instance = view.get_object()
        return instance.order.purchase_date is None


class IsOrderOwner(BasePermission):
    """
    Checks if user is owner the order
    """
    message = "You are not allowed to do this"

    def has_permission(self, request, view):
        instance = view.get_object()
        return instance.user == request.user
