import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile


def get_cover_image() -> SimpleUploadedFile:
    with open(os.path.join(settings.BASE_DIR, "test_data", "test_image.png"), "rb") as file:
        content = file.read()
    return SimpleUploadedFile(name="test_image.jpg", content=content, content_type="image/png")
