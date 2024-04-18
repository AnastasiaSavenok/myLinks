from rest_framework.permissions import BasePermission


class IsVerified(BasePermission):
    """
    Check is current user verified.
    """

    def has_permission(self, request, view):
        return request.user.is_verify


class IsOwner(BasePermission):
    """
    Check is current user object owner.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
