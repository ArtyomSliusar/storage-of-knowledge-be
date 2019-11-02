from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsCreationOrIsAuthenticated(permissions.BasePermission):
    """
    Permission for ViewSet
    create: all
    list: authenticated
    retrieve, update, destroy: authenticated && owner
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            if view.action == 'create':
                return True
            else:
                return False
        else:
            return True

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class IsOwnerOrPublicReadOnly(permissions.BasePermission):
    """
    Permission for ApiView
    POST, PUT, PATCH, DELETE: authenticated && owner
    GET, OPTIONS, HEAD: public - all, private - authenticated && owner
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.private is False or obj.user.id == request.user.id
        else:
            return obj.user.id == request.user.id
