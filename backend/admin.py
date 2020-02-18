from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext as _

from .models import *


# Register your models here.

class UserInline(admin.StackedInline):
    model = User
    extra = 1


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Define admin models for custom User models with no email field."""
    title = "Student"

    """fieldsets = (
        (None, {'fields': ('get_password',)}),
        (_('Personal info'), {'fields': ('get_dni', 'get_email', 'get_first_name', 'get_last_name', 'padron')}),
        (_('Important dates'), {'fields': ('get_last_login', 'get_date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('get_dni', 'get_email', 'user__password1', 'user__password2'),
        }),
    )
    list_display = ('get_dni', 'get_email', 'get_first_name', 'get_last_name', 'padron')
    search_fields = ('get_dni', 'get_email', 'get_first_name', 'get_last_name', 'padron')
    # ordering = ('get_dni', 'get_email', 'get_first_name', 'last_name', 'padron')

    def get_password(self, obj):
        return obj.user.password

    def get_dni(self, obj):
        return obj.user.dni

    def get_email(self, obj):
        return obj.user.email

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_last_login(self, obj):
        return obj.user.last_login

    def get_date_joined(self, obj):
        return obj.user.date_joined

    def get_last_name(self, obj):
        return obj.user.last_name
    """

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

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name',),
        }),
    )

    list_display = ('name', 'list_correlatives')
    search_fields = ('name',)
    ordering = ('name',)

    def list_correlatives(self, obj):
        return [sub.__str__() for sub in obj.correlatives.all()]
