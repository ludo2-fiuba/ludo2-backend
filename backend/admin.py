from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _
from django_reverse_admin import ReverseModelAdmin

from forms import InscribirForm
from .models import *


# Register your models here.
from .models.course import Course


class CourseWithStudentInline(admin.TabularInline):
    model = Course.students.through


class StudentCommonAdmin(ReverseModelAdmin):
    inline_type = 'tabular'
    inline_reverse = [('user', {'fields': ['first_name', 'last_name', 'dni']})]

    list_display = ('dni', 'first_name', 'last_name', 'padron')
    search_fields = ('dni', 'first_name', 'last_name', 'padron')
    readonly_fields = ('dni', 'first_name', 'last_name')
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


@admin.register(Student)
class StudentRegularAdmin(StudentCommonAdmin):
    title = "Regular Student"

    def get_queryset(self, request):
        """
        Filter the objects displayed in the change_list to only
        display those for the currently signed in user.
        """
        qs = super().get_queryset(request)
        return qs.filter(inscripto=False)


class PreRegisteredStudent(Student):
    class Meta:
        proxy = True


@admin.register(PreRegisteredStudent)
class StudentPreRegistered(StudentCommonAdmin):
    title = "Student to Register"

    inlines = [
        CourseWithStudentInline,
    ]

    list_display = ('dni', 'first_name', 'last_name', 'padron', 'inscribir_button')
    readonly_fields = ('dni', 'first_name', 'last_name', 'inscribir_button')

    def get_queryset(self, request):
        """
        Filter the objects displayed in the change_list to only
        display those for the currently signed in user.
        """
        qs = super().get_queryset(request)
        return qs.filter(inscripto=False)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url(r'^(?P<student_id>.+)/inscribir/$',
                self.admin_site.admin_view(self.inscribir),
                name='inscribir')
        ]
        return my_urls + urls

    def inscribir_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Inscribir</a>',
            reverse('admin:inscribir', args=[obj.pk]),
        )

    actions = ['inscribir']

    def inscribir(self, request, student_id):
        student = self.get_object(request, student_id)
        form = InscribirForm(request.POST)
        if form.is_valid():
            try:
                form.save(student)
            except Exception as e:
                # If save() raised, the form will a have a non
                # field error containing an informative message.
                pass
            else:
                self.message_user(request, 'Success')
                url = reverse(
                    'admin:backend_student_changelist',
                    current_app=self.admin_site.name,
                )
                return HttpResponseRedirect(url)

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['student'] = student
        context['title'] = "Inscribir"

        return TemplateResponse(
            request,
            'admin/inscribir_alumno.html',
            context,
        )

    inscribir.short_description = "Inscribir Alumno"


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
    title = "FinalExam"
    title = "Final"

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('final', 'student', 'grade'),
        }),
    )

    list_display = ('student', 'subject', 'date', 'grade')
    search_fields = ('student', 'subject', 'grade')
    ordering = ('student', 'grade')

    def subject(self, obj):
        return obj.final.subject

    def date(self, obj):
        return obj.final.date

    subject.admin_order_field = 'final__subject__name'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    title = "Course"

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('year', 'semester', 'subject', 'teacher'),
        }),
    )

    inlines = [
        CourseWithStudentInline,
    ]
    exclude = ('students',)

    filter_horizontal = ('students',)

    list_display = ('year', 'semester', 'subject', 'teacher')
    search_fields = ('year', 'semester', 'subject', 'teacher')
    ordering = ('year', 'semester', 'subject', 'teacher')


@admin.register(Final)
class FinalAdmin(admin.ModelAdmin):
    title = "Final"

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('subject', 'teacher', 'date'),
        }),
    )

    list_display = ('subject', 'teacher', 'date')
    search_fields = ('subject', 'teacher', 'date')
    ordering = ('subject', 'teacher', 'date')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    title = "Subject"

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'correlatives'),
        }),
    )

    list_display = ('name', 'list_correlatives')
    search_fields = ('name',)
    ordering = ('name',)

    def list_correlatives(self, obj):
        return [sub.__str__() for sub in obj.correlatives.all()]

