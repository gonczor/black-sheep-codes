from django.contrib.auth import get_user_model
from django.db.models import QuerySet

User = get_user_model()


class CourseQuerySet(QuerySet):
    def filter_signed_up(self, user: User):
        return self.filter(signups__user=user)
