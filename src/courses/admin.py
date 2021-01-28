from django.contrib.admin import ModelAdmin, site

from courses.models import Course, CourseSection, CourseSignup


class CourseAdmin(ModelAdmin):
    list_display = ("name",)


class CourseSectionAdmin(ModelAdmin):
    list_display = ("name", "course")


class CourseSignupAdmin(ModelAdmin):
    list_display = ("course", "user")


site.register(Course, CourseAdmin)
site.register(CourseSection, CourseSectionAdmin)
site.register(CourseSignup, CourseSignupAdmin)
