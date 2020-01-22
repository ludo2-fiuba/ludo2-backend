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
