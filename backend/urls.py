from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'subjects', views.SubjectViewSet, 'subject')
router.register(r'final_exams', views.StudentFinalExamViewSet, 'final_exam')
router.register(r'final_exams', views.TeacherFinalExamViewSet, 'final_exam')

schema_view = get_schema_view(
    openapi.Info(
        title="LUDO API",
        default_version='v1',
        description="Endpoint specification of the LUDO API ",
        contact=openapi.Contact(email="fede.est@gmail.com, danielap.riesgo@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # app own routes
    path('api/', include(router.urls)),

    # path to djoser end points
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # swagger endpoints
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
