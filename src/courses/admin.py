from django.contrib.admin import ModelAdmin, site
from django.core.handlers.wsgi import WSGIRequest
from django.forms import ModelForm

from courses.models import Course
from courses.tasks import test_task


class CourseAdmin(ModelAdmin):
    list_display = ('name',)

    def save_model(self, request: WSGIRequest, obj: Course, form: ModelForm, change: bool):
        result = super().save_model(request, obj, form, change)
        test_task.apply_async()
        return result


site.register(Course, CourseAdmin)
