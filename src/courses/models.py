from django.db.models import ImageField, CharField, TextField, Model, DateTimeField
from django.db.models.signals import post_save

from courses.signals import cover_image_resize_callback


class Course(Model):
    name = CharField(max_length=64)
    description = TextField()
    cover_image = ImageField()
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)


post_save.connect(cover_image_resize_callback, sender=Course)
