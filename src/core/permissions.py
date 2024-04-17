from rest_framework.permissions import BasePermission


class IsVerified(BasePermission):
    """
    Check is current user verified.
    """

    def has_permission(self, request, view):
        return request.user.is_verify
