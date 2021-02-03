from rest_framework.routers import SimpleRouter

from lessons.views import LessonViewSet

router = SimpleRouter()
router.register("lessons", LessonViewSet, basename="lessons")


urlpatterns = router.urls
