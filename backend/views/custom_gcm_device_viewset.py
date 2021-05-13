from push_notifications.api.rest_framework import GCMDeviceViewSet
from push_notifications.models import GCMDevice
from rest_framework.permissions import IsAuthenticated

from backend.serializers import CustomGCMDeviceSerializer


class CustomGCMDeviceViewSet(GCMDeviceViewSet):
    queryset = GCMDevice.objects.all()
    serializer_class = CustomGCMDeviceSerializer
    permission_classes = [IsAuthenticated]
