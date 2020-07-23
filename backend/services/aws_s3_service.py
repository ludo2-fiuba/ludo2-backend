import base64
import os

import boto3


def _decode_image(b64_image):
    b64_image = b64_image.lstrip("data:image/jpeg;base64,")
    return base64.b64decode(b64_image)


class AwsS3Service:
    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
        )
        self.bucket = os.environ["AWS_BUCKET_NAME"]

    def upload_b64_image(self, b64_string, file_name):
        self.upload_object(_decode_image(b64_string), file_name)

    def upload_object(self, object, file_name):
        self.client.put_object(Body=object, Bucket=self.bucket, Key=file_name)
