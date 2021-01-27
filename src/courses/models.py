from django.db.models import ImageField, CharField, TextField, Model, DateTimeField
from django.db.models.signals import post_save

import courses.signals


class Course(Model):
    name = CharField(max_length=64)
    description = TextField()
    cover_image = ImageField()
    small_cover_image = ImageField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)


post_save.connect(courses.signals.cover_image_resize_callback, sender=Course)
