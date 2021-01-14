from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import format_html
from django_reverse_admin import ReverseModelAdmin

from .forms import InscribirForm, StaffCreateForm
from .models import *


class StaffUser(User):
    class Meta:
        verbose_name = "Staff User"
        proxy = True


@admin.register(StaffUser)
class StaffUserAdmin(UserAdmin):
    title = "Usuario Administrador"

    list_display = ('id', 'dni', 'email', 'first_name', 'last_name', 'get_groups')
    exclude = ('is_student', 'is_teacher', 'username', 'user_permissions', 'updated_at', 'date_joined', 'last_login')
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

    add_form = StaffCreateForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_staff=True)

    def get_password(self, obj):
        return obj.password

    def get_groups(self, obj):
        return [g.name for g in obj.groups.all()]


class StudentCommonAdmin(admin.ModelAdmin):
    inline_type = 'tabular'
    inline_reverse = [('user', {'fields': ['first_name', 'last_name', 'dni']})]

    list_display = ('dni', 'first_name', 'last_name', 'padron')
    exclude = ("face_encodings", 'inscripto')
    search_fields = ('dni', 'first_name', 'last_name', 'padron')
    readonly_fields = ('dni', 'first_name', 'last_name', 'padron', 'user')

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
        return qs.filter(inscripto=True)


class PreRegisteredStudent(Student):
    class Meta:
        verbose_name = "Pre Registered Student"
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
        form = InscribirForm(request.POST)
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
            'admin/inscribir_alumno.html',
            context,
        )

    inscribir.short_description = "Inscribir Alumno"


@admin.register(Teacher)
class TeacherAdmin(ReverseModelAdmin):
    title = "Teacher"
    inline_type = 'tabular'
    inline_reverse = [('user', {'fields': ['first_name', 'last_name', 'dni']})]

    list_display = ('dni', 'first_name', 'siu_id','last_name', 'legajo')
    exclude = ("face_encodings", )
    search_fields = ('dni', 'first_name', 'siu_id', 'last_name', 'legajo')
    readonly_fields = ('dni', 'first_name', 'siu_id', 'last_name', 'legajo', 'user')

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
        verbose_name = "Final Date to Approve"
        verbose_name_plural = "Final Dates to Approve"
        proxy = True


@admin.register(FinalToApprove)
class FinalToApproveAdmin(admin.ModelAdmin):
    title = "Final Date to Approve"
    fields = ('subject_name', 'teacher', 'date')
    exclude = ('updated_at',)
    readonly_fields = ('subject_name', 'teacher', 'date')

    list_display = ('subject_name', 'teacher', 'date', 'approve', 'reject')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
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

    def approve(self, obj):
        return format_html(
            '<a class="button" href="{}">Aprobar</a>',
            reverse('admin:approve_action', args=[obj.pk]),
        )

    def reject(self, obj):
        return format_html(
            '<a class="button" href="{}">Rechazar</a>',
            reverse('admin:reject_action', args=[obj.pk]),
        )

    actions = ['approve_action', 'reject_action']

    def approve_action(self, request, final_id):
        final = self.get_object(request, final_id)
        final.status = Final.Status.OPEN
        final.save()

        self.message_user(request, f"Final date approved")
        url = reverse(
            'admin:backend_finaltoapprove_changelist',
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(url)

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


@admin.register(Final)
class FinalAdmin(admin.ModelAdmin):
    title = "Final"
    fields = ('subject_name', 'subject_siu_id', 'teacher', 'date', 'qrid')
    exclude = ('updated_at',)
    readonly_fields = ('subject_name', 'subject_siu_id', 'date', 'qrid')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(status__in=(Final.Status.OPEN, Final.Status.PENDING_ACT, Final.Status.ACT_SENT))

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url(r'^(?P<final_id>.+)/download/$',
                self.admin_site.admin_view(self.download),
                name='download')
        ]
        return my_urls + urls

    list_display = ('subject_name', 'subject_siu_id', 'teacher', 'date', 'download_qr')
    search_fields = ('subject_name', 'date',)

    def download_qr(self, obj):
        return format_html(
            '<a class="button" href="{}">Descargar QR</a>',
            reverse('admin:download', args=[obj.pk]),
        )

    actions = ['download']

    def download(self, request, final_id):
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
