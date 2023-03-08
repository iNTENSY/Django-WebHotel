from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_owner = obj.customers == request.user
        if request.method in permissions.SAFE_METHODS and is_owner:
            return True

        return is_owner or request.user.is_staff