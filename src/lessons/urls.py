from rest_framework.routers import SimpleRouter

from lessons.views import CommentViewSet, LessonViewSet

app_name = "lessons"

router = SimpleRouter()
router.register("lessons", LessonViewSet, basename="lesson")
router.register("comments", CommentViewSet, basename="comment")


urlpatterns = router.urls
