from django import template

register = template.Library()


@register.simple_tag
def reject_url(student):
    return f"/admin/backend/preregisteredstudent/{student.user_id}/rechazar/"


@register.simple_tag
def approve_url(student_id):
    return f"/admin/backend/preregisteredstudent/{student_id.user_id}/aprobar/"
