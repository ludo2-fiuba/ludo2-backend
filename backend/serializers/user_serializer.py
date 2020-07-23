from djoser.serializers import UserCreateSerializer

from backend.services import AwsS3Service


class UserCustomCreateSerializer(UserCreateSerializer):
    def create(self, validated_data):
        self._upload_image(self.context['image'], f"{validated_data['dni']}.jpg")
        return super().create(validated_data)


    def _upload_image(self, image_b64, image_name):
        AwsS3Service().upload_b64_image(image_b64, image_name)
