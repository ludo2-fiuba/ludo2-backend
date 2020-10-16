from django.urls import path, include, re_path
from rest_framework import routers

from . import views
from .views.user_views import UserCustomViewSet

router = routers.DefaultRouter()
router.register(r'final_exams', views.FinalStudentExamViewSet, 'final_exam')
router.register(r'final_exams', views.FinalTeacherExamViewSet, 'final_exam')
router.register(r'finals', views.FinalTeacherViewSet, 'final')
router.register(r'courses', views.CourseTeacherViewSet, 'course')

auth_router = routers.DefaultRouter()
auth_router.register(r'auth/users', UserCustomViewSet)

urlpatterns = [
    # app own routes
    path('api/', include(router.urls)),

    # path to djoser end points
    # path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('', include(auth_router.urls)),

    # swagger endpoints
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
