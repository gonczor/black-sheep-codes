from rest_framework.routers import SimpleRouter

from courses.views import CourseSignupView, CourseViewSet, TestView

app_name = "courses"

router = SimpleRouter()
router.register("courses", CourseViewSet)
router.register("course-signups", CourseSignupView, basename="course_signups")
router.register("tst", TestView, basename="tst")

urlpatterns = router.urls
