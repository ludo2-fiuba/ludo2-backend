from djoser.serializers import UserCreateSerializer

from backend.services import AwsS3Service

from backend.utils import user_image_path


class UserCustomCreateSerializer(UserCreateSerializer):
    def create(self, validated_data):
        self._upload_image(self.context['image'], user_image_path(validated_data['dni']))
        return super().create(validated_data)


    def _upload_image(self, image_b64, image_name):
        AwsS3Service().upload_b64_image(image_b64, image_name)
