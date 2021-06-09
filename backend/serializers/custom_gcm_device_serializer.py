from push_notifications.api.rest_framework import GCMDeviceSerializer, DeviceSerializerMixin
from push_notifications.models import GCMDevice


class CustomGCMDeviceSerializer(GCMDeviceSerializer):
    class Meta(DeviceSerializerMixin.Meta):
        model = GCMDevice
        fields = (
            "id", "name", "user", "registration_id", "device_id", "active", "date_created",
            "cloud_message_type", "application_id",
        )
        extra_kwargs = {"id": {"read_only": False, "required": False}}

    def create(self, validated_data):
        """Override ``create`` to provide a user via request.user by default.
        This is required since the read_only ``user`` field is not included by
        default anymore since
        https://github.com/encode/django-rest-framework/pull/5886.
        """
        if 'user' not in validated_data:
            validated_data['user'] = self.context['request'].user
        if GCMDevice.objects.exists(user=self.context['request'].user):
            device = GCMDevice.objects.filter(user=self.context['request'].user).last()
            return super(GCMDeviceSerializer, self).update(device, validated_data)
        return super(GCMDeviceSerializer, self).create(validated_data)
