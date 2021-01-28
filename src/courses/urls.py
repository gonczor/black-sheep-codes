from rest_framework.routers import SimpleRouter

from courses.views import CourseSignupView, CourseViewSet

app_name = "courses"

router = SimpleRouter()
router.register("courses", CourseViewSet)
router.register("course-signups", CourseSignupView, basename="course_signups")

urlpatterns = router.urls
