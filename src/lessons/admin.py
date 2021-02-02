from django.contrib.admin import ModelAdmin, site

from lessons.models import Lesson, Exercise, Test


class BaseLessonAdmin(ModelAdmin):
    list_display = ("name", "course_section")


site.register(Lesson, BaseLessonAdmin)
site.register(Exercise, BaseLessonAdmin)
site.register(Test, BaseLessonAdmin)
