from django.urls import include, path, re_path
from rest_framework_nested import routers

from . import views
from .views import CustomGCMDeviceViewSet
from .views.user_views import UserCustomViewSet

router = routers.SimpleRouter()
router.register(r'final_exams', views.FinalExamStudentViewSet, 'final_exam')
router.register(r'finals', views.FinalTeacherViewSet, 'final')
router.register(r'subjects', views.SubjectViewSet, 'subject')
router.register(r'commissions', views.CommissionViewSet, 'commission')
router.register(r'device/gcm', CustomGCMDeviceViewSet)

teacher_finals_router = routers.NestedSimpleRouter(router, r'finals', lookup='final')
teacher_finals_router.register(r'final_exams', views.FinalExamTeacherViews, basename='final-final_exams')

auth_router = routers.DefaultRouter()
auth_router.register(r'auth/users', UserCustomViewSet)

urlpatterns = [
    # app own routes
    path('api/', include(router.urls)),
    path('api/', include(teacher_finals_router.urls)),

    # path to djoser end points
    path('auth/', include('djoser.urls.jwt')),

    path('', include(auth_router.urls)),
    re_path(r'^auth/oauth/$', views.user_views.token_obtain_pair, name='api-oauth'),
]
