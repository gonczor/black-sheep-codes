from django.db.models import ImageField, CharField, TextField, Model, DateTimeField


class Course(Model):
    name = CharField(max_length=64)
    description = TextField()
    cover_image = ImageField()
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
