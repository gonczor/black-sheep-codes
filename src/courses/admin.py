from django.contrib.admin import ModelAdmin, site

from courses.models import Course, CourseSection


class CourseAdmin(ModelAdmin):
    list_display = ("name",)


class CourseSectionAdmin(ModelAdmin):
    list_display = ("name", "course")


site.register(Course, CourseAdmin)
site.register(CourseSection, CourseSectionAdmin)
