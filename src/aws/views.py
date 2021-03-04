from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from rest_framework import status


def health_check(request: WSGIRequest) -> HttpResponse:
    return HttpResponse(status=status.HTTP_200_OK)
