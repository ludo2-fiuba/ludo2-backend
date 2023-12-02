from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_nested import routers

from . import views
from .views import CustomGCMDeviceViewSet
from .views.user_views import UserCustomViewSet

router = routers.SimpleRouter()
router.register(r'final_exams', views.FinalExamStudentViewSet, 'final_exam')
router.register(r'finals', views.FinalTeacherViewSet, 'final')
router.register(r'subjects', views.SubjectViewSet, 'subject')
router.register(r'commissions', views.CommissionViewSet, 'commission')
router.register(r'teacher/commissions', views.CommissionTeacherViewSet, 'commission')
router.register(r'semesters', views.SemesterViewSet, 'semester')
router.register(r'evaluations', views.EvaluationViewSet, 'evaluation')
router.register(r'evaluations/submissions', views.EvaluationSubmissionViewSet, 'evaluation')
router.register(r'teacher/evaluations', views.EvaluationTeacherViewSet, 'evaluation')
router.register(r'teacher/evaluations/submissions', views.EvaluationSubmissionTeacherViewSet, 'evaluation')
router.register(r'commission_inscription', views.CommissionInscriptionViewSet, 'commission_inscription')
router.register(r'device/gcm', CustomGCMDeviceViewSet)

teacher_finals_router = routers.NestedSimpleRouter(router, r'finals', lookup='final')
teacher_finals_router.register(r'final_exams', views.FinalExamTeacherViews, basename='final-final_exams')

auth_router = routers.DefaultRouter()
auth_router.register(r'auth/users', UserCustomViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="LUDO API",
        default_version='v1',),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # app own routes
    path('api/', include(router.urls)),
    path('api/', include(teacher_finals_router.urls)),

    # path to djoser end points
    path('auth/', include('djoser.urls.jwt')),

    path('', include(auth_router.urls)),
    re_path(r'^auth/oauth/$', views.user_views.token_obtain_pair, name='api-oauth'),
    
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui')
]
