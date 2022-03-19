from rest_framework import permissions


class AuthorOrAuthenticatedReadOnly(permissions.BasePermission):
    """
    Права доступа для автора и аутентифицированного пользователя.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Права доступа для админа и только для чтения.
    """
    def has_permission(self, request, view):
        user = request.user
        return (
            request.method in permissions.SAFE_METHODS
            or (
                user.is_authenticated and user.is_admin()
            )
        )
