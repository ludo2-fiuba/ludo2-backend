from django.urls import path, include  # add this
from rest_framework import routers  # add this
from . import views

router = routers.DefaultRouter()
router.register(r'students', views.StudentsViewSet, 'student')

urlpatterns = [
    path('', views.index, name='index'),

    # path to djoser end points
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('api/', include(router.urls))
]
