from rest_framework.permissions import BasePermission


class SuperviserRankRequiredPermission(BasePermission):

    def has_permission(self, request, view):
        return None


class OperatorRankRequiredPermission(BasePermission):

    def has_permission(self, request, view):
        return None


class ContentManagerRankRequiredPermission(BasePermission):

    def has_permission(self, request, view):
        return None


class ArticleWriterRankRequiredPermission(BasePermission):

    def has_permission(self, request, view):
        return None


class PackagerRankRequiredPermission(BasePermission):

    def has_permission(self, request, view):
        return None
