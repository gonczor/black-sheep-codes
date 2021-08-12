from django.urls import path
from django.views.generic import TemplateView

from .views import ActivationView

app_name = "frontend"

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html")),
    path("activation/<str:uid>/<str:token>/", ActivationView.as_view()),
    path("gdpr/", TemplateView.as_view(template_name="privacy_policy.html")),
    path("login/", TemplateView.as_view(template_name="login.html"), name="login"),
    path("courses/", TemplateView.as_view(template_name="courses.html")),
    path("courses/<int:id>/", TemplateView.as_view(template_name="course_details.html")),
]
