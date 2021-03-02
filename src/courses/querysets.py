from django.db.models import Prefetch, QuerySet

from auth_ex.models import User


class CourseQuerySet(QuerySet):
    def filter_signed_up(self, user: User):
        return self.filter(signups__user=user)

    def with_completed_lessons(self, user: User):
        from lessons.models import BaseLesson

        return self.prefetch_related(
            "course_sections",
            Prefetch(
                "course_sections__lessons",
                queryset=BaseLesson.objects.all().with_completed_annotations(user=user),
            ),
        )
