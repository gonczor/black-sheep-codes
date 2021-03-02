from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class ProcessingException(Exception):
    default_detail = _("Can't process the request.")
    detail = None

    def __init__(self, detail=None):
        self.detail = detail or self.default_detail


class ProcessingApiException(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
