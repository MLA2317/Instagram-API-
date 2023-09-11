from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admin to edit/delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Admin permissions
        if request.user.is_staff:
            return True

        # Owner permissions
        return obj.user_id == request.user
