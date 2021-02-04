from rest_framework.routers import SimpleRouter

from lessons.views import LessonViewSet

app_name = "lessons"

router = SimpleRouter()
router.register("lessons", LessonViewSet, basename="lesson")


urlpatterns = router.urls
