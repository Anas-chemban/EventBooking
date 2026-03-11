from rest_framework.permissions import BasePermission


class IsEventOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and
            obj.created_by == request.user
        )
