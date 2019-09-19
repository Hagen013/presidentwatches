from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        user_pk = request.GET.get('user')
        user = request.user
        if user_pk == user.id:
            return True
        else:
            return False
