from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    All authenticated users can read,
    but only administrators can edit.
    """

    def has_permission(self, request, view):
        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated

        return request.user and request.user.is_staff