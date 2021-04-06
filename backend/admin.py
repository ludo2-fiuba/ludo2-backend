import os
import collections
import functools

from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import format_html

from .forms import RegisterForm, StaffCreateForm
from .models import *
from .services.siu_service import SiuService


class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        return self.func.__doc__

    def __get__(self, obj, objtype):
        return functools.partial(self.__call__, obj)


@memoized
def departments():
    return SiuService().list_departments()

@memoized
def subjects():
    return SiuService().list_subjects()


class StaffUser(User):
    class Meta:
        verbose_name = "Usuario Administrador"
        verbose_name_plural = "Usuarios Administradores"
        proxy = True


class StaffInline(admin.TabularInline):
    model = Staff
    fieldsets = [
        (None, {
            'fields': ('department_siu_id',)
            }),
        ]


@admin.register(StaffUser)
class StaffUserAdmin(UserAdmin):
    inlines = [StaffInline]

    exclude = ('user_permissions', 'is_student', 'is_teacher', 'date_joined', 'username', 'last_login', 'active', 'password', 'updated_at', 'is_staff', 'is_superuser')
    can_delete = False
    list_display = ('dni', 'first_name', 'last_name', 'department_siu_id')
    search_fields = ('dni', 'first_name', 'last_name', 'department_siu_id')
    ordering = ('dni', 'first_name', 'last_name')

    add_form = StaffCreateForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'dni', 'first_name', 'last_name', 'password1', 'password2', 'groups')}
        ),
    )

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'dni', 'first_name', 'last_name', 'groups')}
        ),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_staff=True)

    def department_siu_id(self, obj):
        return obj.staff.department_siu_id

    department_siu_id.short_description = "SIU ID del Departamento"


class StudentCommonAdmin(admin.ModelAdmin):
    inline_type = 'tabular'
    inline_reverse = [('user', {'fields': ['first_name', 'last_name', 'dni']})]

    list_display = ('dni', 'first_name', 'last_name', 'padron')
    exclude = ("face_encodings", 'inscripto', 'user')
    search_fields = ('dni', 'first_name', 'last_name', 'padron')
    readonly_fields = ('dni', 'first_name', 'last_name', 'padron')
    ordering = ('padron',)

    def get_password(self, obj):
        return obj.user.password

    def dni(self, obj):
        return obj.user.dni
    dni.short_description = "DNI"

    def first_name(self, obj):
        return obj.user.first_name
    first_name.short_description = "Nombre"

    def last_name(self, obj):
        return obj.user.last_name
    last_name.short_description = "Apellido"

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
        return qs.filter(inscripto=True)


class PreRegisteredStudent(Student):
    class Meta:
        verbose_name = "Estudiante pre registrado"
        verbose_name_plural = "Estudiantes pre registrados"
        proxy = True


@admin.register(PreRegisteredStudent)
class StudentPreRegistered(StudentCommonAdmin):
    title = "Student to Register"

    list_display = ('dni', 'first_name', 'last_name', 'inscribir_button')
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
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                form.save(student)
            except Exception as e:
                # If save() raised, the form will a have a non
                # field error containing an informative message.
                pass
            else:
                self.message_user(request, f"Success. Student {student} for registered")
                url = reverse(
                    'admin:backend_preregisteredstudent_changelist',
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
            'admin/register_student.html',
            context,
        )

    inscribir.short_description = "Inscribir Alumno"


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    inline_type = 'tabular'
    inline_reverse = [('user', {'fields': ['first_name', 'last_name', 'dni']})]

    list_display = ('dni', 'first_name', 'last_name', 'siu_id', 'legajo')
    exclude = ("face_encodings", 'user')
    search_fields = ('dni', 'first_name', 'last_name', 'siu_id', 'legajo')
    readonly_fields = ('dni', 'first_name', 'last_name', 'siu_id', 'legajo')
    ordering = ('legajo',)

    def get_password(self, obj):
        return obj.user.password

    def dni(self, obj):
        return obj.user.dni
    dni.short_description = "DNI"

    def first_name(self, obj):
        return obj.user.first_name
    first_name.short_description = "Nombre"

    def last_name(self, obj):
        return obj.user.last_name
    last_name.short_description = "Apellido"

    def get_last_login(self, obj):
        return obj.user.last_login

    def get_date_joined(self, obj):
        return obj.user.date_joined


@admin.register(FinalExam)
class FinalExamAdmin(admin.ModelAdmin):
    title = "FinalExam"

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('final', 'student', 'grade'),
        }),
    )

    list_display = ('subject', 'student', 'date', 'grade')
    search_fields = ('student', 'grade')
    ordering = ('student', 'grade')
    readonly_fields = ('final', 'student', 'grade')

    def date(self, obj):
        return obj.final.date

    def subject(self, obj):
        return obj.final.subject_name


class FinalToApprove(Final):
    class Meta:
        verbose_name = "Fecha para aprobar"
        verbose_name_plural = "Fechas para aprobar"
        proxy = True


@admin.register(FinalToApprove)
class FinalToApproveAdmin(admin.ModelAdmin):
    title = "Final Date to Approve"
    fields = ('subject_name', 'teacher', 'date')
    exclude = ('updated_at',)
    readonly_fields = ('subject_name', 'department', 'teacher', 'date')
    list_display = ('subject_name', 'department', 'teacher', 'date', 'approve', 'reject')
    ordering = ('subject_name', 'teacher', 'date')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            owning_subjects = SiuService().list_subjects({"departamentoId": request.user.staff.department_siu_id})
            qs = qs.filter(subject_siu_id__in=[s["department_id"] for s in owning_subjects])
        return qs.filter(status=Final.Status.DRAFT)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url(r'^(?P<final_id>.+)/approve/$',
                self.admin_site.admin_view(self.approve_action),
                name='approve_action'),
            url(r'^(?P<final_id>.+)/reject/$',
                self.admin_site.admin_view(self.reject_action),
                name='reject_action'),
        ]
        return my_urls + urls

    def department(self, obj):
        for subject in subjects():
            if subject['id'] == obj.subject_siu_id:
                for department in departments():
                    if department['id'] == subject['department_id']:
                        return department['name']
    department.short_description="Departamento"

    def approve(self, obj):
        return format_html(
            '<a class="button" href="{}">Aprobar</a>',
            reverse('admin:approve_action', args=[obj.pk]),
        )
    approve.short_description="Aprobar"

    def reject(self, obj):
        return format_html(
            '<a class="button" href="{}">Rechazar</a>',
            reverse('admin:reject_action', args=[obj.pk]),
        )
    reject.short_description = "Rechazar"

    actions = ['approve_action', 'reject_action']

    def approve_action(self, request, final_id):
        final = self.get_object(request, final_id)

        siu_final = SiuService().create_final(final.teacher.siu_id, final.subject_siu_id,
                                              int(final.date.timestamp()))

        final.siu_id = siu_final["id"]
        final.status = Final.Status.OPEN
        final.save()

        self.message_user(request, "Final date approved")
        url = reverse(
            'admin:backend_finaltoapprove_changelist',
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(url)
    approve_action.short_description = "Aprobar Fechas"

    def reject_action(self, request, final_id):
        final = self.get_object(request, final_id)
        final.status = Final.Status.REJECTED
        final.save()

        self.message_user(request, f"Final date rejected", level=messages.WARNING)
        url = reverse(
            'admin:backend_finaltoapprove_changelist',
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(url)
    reject_action.short_description = "Rechazar Fechas"


@admin.register(Final)
class FinalAdmin(admin.ModelAdmin):
    title = "Final"
    fields = ('subject_name', 'department', 'teacher', 'date', 'qrid')
    exclude = ('updated_at',)
    readonly_fields = ('subject_name', 'subject_siu_id', 'date', 'qrid')
    ordering = ('subject_name', 'teacher', 'date')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            owning_subjects = SiuService().list_subjects({"departamentoId": request.user.staff.department_siu_id})
            qs = qs.filter(subject_siu_id__in=[s["id"] for s in owning_subjects])
        return qs.filter(status__in=(Final.Status.OPEN, Final.Status.PENDING_ACT, Final.Status.ACT_SENT))

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url(r'^(?P<final_id>.+)/download/$',
                self.admin_site.admin_view(self.download_action),
                name='download_action')
        ]
        return my_urls + urls

    list_display = ('subject_name', 'department', 'teacher', 'date', 'download_qr')
    search_fields = ('subject_name', 'date',)

    def department(self, obj):
        for subject in subjects():
            if subject['id'] == obj.subject_siu_id:
                for department in departments():
                    if department['id'] == subject['department_id']:
                        return department['name']
    department.short_description = "Departamento"

    def download_qr(self, obj):
        return format_html(
            '<a class="button" href="{}">Descargar QR</a>',
            reverse('admin:download_action', args=[obj.pk]),
        )
    download_qr.short_description="Descargar QR"

    actions = ['download_action']

    def download_action(self, request, final_id):
        import qrcode
        import io

        final = self.get_object(request, final_id)

        qr = qrcode.make(final.qrid)

        output = io.BytesIO()
        qr.save(output, format='PNG')
        file = output.getvalue()

        file_response = HttpResponse(file, content_type='image/png')
        file_response['Content-Disposition'] = f"attachment; filename={final.teacher.user.last_name}-{final.date.strftime('%Y-%m-%d_%H_%M')}.png"
        return file_response
    download_action.short_description="Descargar QR"
