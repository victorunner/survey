from rest_framework import permissions


class AnswerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True

        is_auth = request.user and request.user.is_authenticated
        is_admin = request.user and request.user.is_staff

        if request.method == 'GET':
            if not is_auth:
                return False
            if is_admin:
                return True
            return 'pk' in request.parser_context['kwargs']

        return is_auth

    def has_object_permission(self, request, view, obj):
        is_admin = request.user and request.user.is_staff

        if is_admin:
            if request.method in ['PUT', 'PATCH']:
                return request.user == obj.user
            return True
        return request.user == obj.user


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user and request.user.is_staff
        )
