from django.contrib.admin import site
from django.contrib.auth import admin

from auth_ex.models import User


class UserAdmin(admin.UserAdmin):
    pass


site.register(User, UserAdmin)
