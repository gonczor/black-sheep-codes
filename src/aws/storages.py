import boto3
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage


class BlackSheepS3StaticStorage(S3StaticStorage):
    location = "static/"


class BlackSheepS3MediaStorage(S3Boto3Storage):
    location = "media/"

    def url(self, name, parameters=None, expire=600, http_method="GET"):
        params = {
            "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
            "Key": f"{self.location}{name}",
        }
        resp = self.bucket.meta.client.generate_presigned_url(
            "get_object", Params=params, ExpiresIn=expire, HttpMethod=http_method
        )

        return resp
