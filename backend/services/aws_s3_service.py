import os
import io

import boto3

from backend.utils import decode_image


class AwsS3Service:
    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
        )
        self.bucket = os.environ["AWS_BUCKET_NAME"]
        self.s3_api_url = os.getenv("AWS_DOMAIN_URL", "s3.amazonaws.com")

    def upload_b64_image(self, b64_string, file_name):
        return self.upload_object(io.BytesIO(decode_image(b64_string)), file_name)

    def upload_object(self, generic_object, file_name):
        self.client.upload_fileobj(generic_object, self.bucket, file_name)
        return f"https://{self.bucket}.{self.s3_api_url}/{file_name}"

    def download_object(self, file_name):
        return self.client.get_object(Bucket=self.bucket, Key=file_name)['Body']
