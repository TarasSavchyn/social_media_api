from rest_framework import permissions

class IsProfileOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            permissions.IsAuthenticated().has_permission(request, view) and
            (request.method in permissions.SAFE_METHODS or obj.user == request.user)
        )