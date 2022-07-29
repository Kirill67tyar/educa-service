from rest_framework.permissions import BasePermission


class IsEnrolledPermission(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj) -> True | False:
        return obj.students.filter(pk=request.user.pk).exists()
