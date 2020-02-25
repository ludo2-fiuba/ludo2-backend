from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    """
    Custom permission to only allow students
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_student
