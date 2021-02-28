from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Prefetch, QuerySet

User = get_user_model()


class CourseQuerySet(QuerySet):
    def filter_signed_up(self, user: User):
        return self.filter(signups__user=user)

    def with_completed_lessons(self, user: settings.AUTH_USER_MODEL):
        from lessons.models import BaseLesson

        return self.prefetch_related(
            "course_sections",
            Prefetch(
                "course_sections__lessons",
                queryset=BaseLesson.objects.all().with_completed_annotations(user=user),
            ),
        )
