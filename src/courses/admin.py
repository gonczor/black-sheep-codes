from django.contrib.admin import ModelAdmin, site
from django.core.handlers.wsgi import WSGIRequest
from django.forms import ModelForm

from courses.models import Course


class CourseAdmin(ModelAdmin):
    list_display = ('name',)

    def save_model(self, request: WSGIRequest, obj: Course, form: ModelForm, change: bool):
        return super().save_model(request, obj, form, change)


site.register(Course, CourseAdmin)
