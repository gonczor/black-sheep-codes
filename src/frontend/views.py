import requests
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.views.generic import TemplateView
from rest_framework import status


class ActivationView(TemplateView):
    template_name = "activation.html"

    def get(self, request, uid, token, **kwargs):
        payload = {"uid": uid, "token": token}
        response = requests.post(f"{settings.HOST}api/v1/auth/users/activation/", data=payload)
        if response.status_code != status.HTTP_204_NO_CONTENT:
            return HttpResponseBadRequest(b"Bad request")
        return super().get(request)
