from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext as _
from django_reverse_admin import ReverseModelAdmin
from .models import *


# Register your models here.

@admin.register(Student)
class StudentAdmin(ReverseModelAdmin):
    """Define admin models for custom User models with no email field."""
    title = "Student"
    inline_type = 'tabular'
    inline_reverse = [('user', {'fields': ['first_name', 'last_name', 'dni']})]

    list_display = ('dni', 'first_name', 'last_name', 'padron')
    search_fields = ('dni', 'first_name', 'last_name', 'padron')
    # ordering = ('dni', 'first_name', 'last_name', 'padron')

    def get_password(self, obj):
        return obj.user.password

    def dni(self, obj):
        return obj.user.dni

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def get_last_login(self, obj):
        return obj.user.last_login

    def get_date_joined(self, obj):
        return obj.user.date_joined


@admin.register(Teacher)
class TeacherAdmin(ReverseModelAdmin):
    title = "Teacher"
    inline_type = 'tabular'
    inline_reverse = [('user', {'fields': ['first_name', 'last_name', 'dni']})]

    list_display = ('dni', 'first_name', 'last_name', 'legajo', 'subjects')
    # search_fields = ('dni', 'first_name', 'last_name', 'legajo')
    # ordering = ('dni'', 'first_name', 'last_name', 'legajo')

    def get_password(self, obj):
        return obj.user.password

    def dni(self, obj):
        return obj.user.dni

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def subjects(self, obj):
        return [sub.__str__() for sub in Subject.objects.filter(final__teacher=obj).distinct()]

    def get_last_login(self, obj):
        return obj.user.last_login

    def get_date_joined(self, obj):
        return obj.user.date_joined


@admin.register(FinalExam)
class FinalExamAdmin(admin.ModelAdmin):
    """Define admin models for custom User models with no email field."""
    title = "FinalExam"

    list_display = ('student', 'subject', 'date', 'grade')
    search_fields = ('student', 'subject', 'grade')
    ordering = ('student', 'grade',)

    def subject(self, obj):
        return obj.final.subject

    def date(self, obj):
        return obj.final.date

    subject.admin_order_field = 'final__subject__name'


@admin.register(Final)
class FinalAdmin(admin.ModelAdmin):
    """Define admin models for custom User models with no email field."""
    title = "Final"

    list_display = ('subject', 'teacher', 'date')
    search_fields = ('subject', 'teacher', 'date')
    ordering = ('subject', 'teacher', 'date')


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

