from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from courses.models import CourseSignup
from lessons.models import Answer, Comment, Lesson, Test, TestQuestion
from lessons.tests import BaseCommentTestCase, BaseLessonTestCase


class LessonAPITestCase(APITestCase, BaseLessonTestCase):
    def setUp(self):
        super().setUp()
        self.mark_as_complete_url = reverse(
            "lessons:lesson-mark_as_complete", args=(self.lesson.id,)
        )
        self.revert_mark_as_complete_url = reverse(
            "lessons:lesson-revert_mark_as_complete", args=(self.lesson.id,)
        )
        self.lesson_create_url = reverse("lessons:lesson-list")
        User = get_user_model()
        self.user = User.objects.create_user(
            username="test", email="test@example.com", password="test"
        )
        CourseSignup.objects.create(course=self.course, user=self.user)

    def test_mark_as_complete(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(self.mark_as_complete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(self.lesson.is_completed_by(self.user))

    def test_revert_mark_as_complete(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(self.revert_mark_as_complete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.lesson.is_completed_by(self.user))

    def test_mark_as_complete_duplicate(self):
        self.client.force_authenticate(self.user)
        self.lesson.complete(self.user)

        response = self.client.patch(self.mark_as_complete_url)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_nested_test_lesson_serializer(self):
        self.user.is_superuser = True
        self.user.save()
        create_data = {
            "course_section": self.course_section.id,
            "name": "Some Test",
            "lesson_type": "Test",
            "questions": [
                {
                    "text": 'How to print "Hello, world!"?',
                    "answers": [
                        {"text": 'System.out.println("Hello, world!");', "is_correct": False},
                        {"text": 'print("Hello, world!")', "is_correct": True},
                    ],
                },
            ],
        }
        self.client.force_authenticate(self.user)

        import json

        create_data = json.dumps(create_data)
        response = self.client.post(
            self.lesson_create_url, data=create_data, content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Test.objects.filter(course_section=self.course_section).exists())
        self.assertTrue(
            TestQuestion.objects.filter(test__course_section=self.course_section).exists()
        )
        self.assertEqual(
            Answer.objects.filter(question__test__course_section=self.course_section).count(), 2
        )

    def test_number_of_queries_on_list(self):
        self.client.force_authenticate(self.user)

        # Without prefetch there were 8.
        with self.assertNumQueries(5):
            self.client.get(self.lesson_create_url)


class CommentsApiTestCase(APITestCase, BaseCommentTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.author)

    def test_filter_by_lesson(self):
        different_lesson = Lesson.objects.create(course_section=self.course_section)
        Comment.objects.create(author=self.author, text="Something else", lesson=different_lesson)
        url = self.list_url + f"?lesson={self.lesson.pk}"

        response = self.client.get(url)

        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], self.comment.pk)

    def test_list_without_filtering(self):
        different_lesson = Lesson.objects.create(course_section=self.course_section)
        different_comment = Comment.objects.create(
            author=self.author, text="Something else", lesson=different_lesson
        )

        response = self.client.get(self.list_url)

        ids = [result["id"] for result in response.data["results"]]
        self.assertEqual(len(response.data["results"]), 2)
        self.assertIn(different_comment.pk, ids)
        self.assertIn(self.comment.pk, ids)

    def test_list_contents(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.data["results"][0],
            {"id": self.comment.pk, "author": self.author.username, "text": self.comment.text},
        )

    def test_create(self):
        create_text = "This is a new comment"
        data = {"lesson": self.lesson.pk, "text": create_text}

        response = self.client.post(self.list_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(Comment.objects.first().text, create_text)
        self.assertEqual(Comment.objects.first().author, self.author)

    def test_delete(self):
        User = get_user_model()
        comment_pk = self.comment.pk
        super_user = User.objects.create_user(
            username="super", email="super@example.com", password="test", is_superuser=True
        )
        self.client.force_authenticate(super_user)

        self.client.delete(self.detail_url)

        self.assertTrue(Comment.deleted_objects.filter(id=comment_pk).exists())

    def test_update(self):
        new_text = "New comment message"
        data = {"text": new_text}

        self.client.patch(self.detail_url, data=data)

        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, new_text)

    def test_update_with_lesson_id(self):
        different_lesson = Lesson.objects.create(course_section=self.course_section)
        data = {"text": "New comment message", "lesson": different_lesson.pk}

        response = self.client.patch(self.detail_url, data=data)

        self.comment.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.comment.lesson_id, self.lesson.pk)
