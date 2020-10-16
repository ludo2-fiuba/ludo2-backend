from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import format_html
from django_reverse_admin import ReverseModelAdmin

from .forms import InscribirForm, StaffCreateForm
from .models import *
from .models.course import Course


@admin.register(User)
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
        return qs.filter(inscripto=True)


class PreRegisteredStudent(Student):
    class Meta:
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

    list_display = ('dni', 'first_name', 'last_name', 'legajo', 'courses')
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

    def courses(self, obj):
        return [sub.__str__() for sub in Course.objects.filter(teacher=obj).distinct()]

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
        return obj.final.course.subject

    def date(self, obj):
        return obj.final.date


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    title = "Course"
    fields = ('teacher','subject', 'semester')
    readonly_fields = ('subject', 'semester')

    list_display = ('semester', 'subject', 'teacher')
    search_fields = ('semester', 'subject', 'teacher')
    ordering = ('semester', 'subject', 'teacher')

    def subject(self, obj):
        return obj.course.subject


@admin.register(Final)
class FinalAdmin(admin.ModelAdmin):
    title = "Final"
    # fields = ('subject', 'teacher', 'date')
    exclude = ('updated_at',)
    readonly_fields = ('date', 'course', 'qrid')

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url(r'^(?P<final_id>.+)/download/$',
                self.admin_site.admin_view(self.download),
                name='download')
        ]
        return my_urls + urls

    list_display = ('subject', 'teacher', 'date', 'download_qr')
    search_fields = ('subject', 'teacher', 'date')
    # ordering = ('subject', 'teacher', 'date')

    def subject(self, obj):
        return obj.course.subject

    def teacher(self, obj):
        return obj.course.teacher

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
        file_response['Content-Disposition'] = f"attachment; filename={final.teacher().user.last_name}-{final.date}.png"
        return file_response
