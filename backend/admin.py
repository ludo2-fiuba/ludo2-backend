from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext as _

from .models import *


# Register your models here.

@admin.register(Student)
class StudentAdmin(DjangoUserAdmin):
    """Define admin models for custom User models with no email field."""
    title = "Student"

    fieldsets = (
        (None, {'fields': ('password',)}),
        (_('Personal info'), {'fields': ('dni', 'email', 'first_name', 'last_name', 'padron')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('dni', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('dni', 'email', 'first_name', 'last_name', 'padron', 'is_staff')
    search_fields = ('dni', 'email', 'first_name', 'last_name', 'padron')
    ordering = ('dni', 'email', 'first_name', 'last_name', 'padron')


@admin.register(FinalExam)
class FinalExamAdmin(admin.ModelAdmin):
    """Define admin models for custom User models with no email field."""
    title = "FinalExam"

    list_display = ('grade', 'subject', 'student')
    search_fields = ('grade', 'subject', 'student')
    ordering = ('grade',)

    def subject(self, obj):
        return obj.final.subject

    subject.admin_order_field = 'final__subject__name'


@admin.register(Final)
class FinalAdmin(admin.ModelAdmin):
    """Define admin models for custom User models with no email field."""
    title = "Final"

    list_display = ('subject', 'date')
    search_fields = ('subject', 'date')
    ordering = ('subject', 'date')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Define admin models for custom User models with no email field."""
    title = "Subject"

    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
