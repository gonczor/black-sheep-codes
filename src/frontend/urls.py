from django.conf import settings
from django.urls import path
from django.views.generic import TemplateView

from .views import ActivationView

app_name = "frontend"

urlpatterns = [
    path(
        "",
        TemplateView.as_view(
            template_name="index.html", extra_context={"running_prod": not settings.DEBUG}
        ),
    ),
    path(
        "activation/<str:uid>/<str:token>/",
        ActivationView.as_view(extra_context={"running_prod": not settings.DEBUG}),
    ),
    path(
        "gdpr/",
        TemplateView.as_view(
            template_name="privacy_policy.html", extra_context={"running_prod": not settings.DEBUG}
        ),
    ),
    path(
        "login/",
        TemplateView.as_view(
            template_name="login.html", extra_context={"running_prod": not settings.DEBUG}
        ),
        name="login",
    ),
    path(
        "courses/",
        TemplateView.as_view(
            template_name="courses.html", extra_context={"running_prod": not settings.DEBUG}
        ),
    ),
    path(
        "courses/<int:id>/",
        TemplateView.as_view(
            template_name="course_details.html", extra_context={"running_prod": not settings.DEBUG}
        ),
    ),
]
