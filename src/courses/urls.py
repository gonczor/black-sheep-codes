from rest_framework.routers import SimpleRouter

from courses.views import CourseViewSet

app_name = "courses"

router = SimpleRouter()
router.register("courses", CourseViewSet)

urlpatterns = router.urls
