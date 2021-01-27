from django.contrib.admin import ModelAdmin, site

from courses.models import Course


class CourseAdmin(ModelAdmin):
    list_display = ("name",)


site.register(Course, CourseAdmin)
