from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    """
    Custom permission to only allow students
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_student


class IsTeacher(permissions.BasePermission):
    """
    Custom permission to only allow students
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_teacher


class IsPostRequest(permissions.BasePermission):
    """
    Custom permission to be used in POST methods
    """
    def has_permission(self, request, view):
        return request.method == "POST"


class IsPutRequest(permissions.BasePermission):
    """
    Custom permission to be used in PUT methods
    """
    def has_permission(self, request, view):
        return request.method == "PUT"
