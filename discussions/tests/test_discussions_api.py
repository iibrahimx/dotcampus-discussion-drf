from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from discussions.models import Discussion, Comment


class DiscussionAPITests(APITestCase):
    def setUp(self):
        self.learner = User.objects.create_user(
            username="learner", password="Pass12345", role="learner"
        )
        self.mentor = User.objects.create_user(
            username="mentor", password="Pass12345", role="mentor"
        )
        self.admin = User.objects.create_user(
            username="admin", password="Pass12345", role="admin"
        )

        self.learner_discussion = Discussion.objects.create(
            author=self.learner, title="Learner Post", content="Learner content"
        )
        self.other_discussion = Discussion.objects.create(
            author=self.mentor, title="Mentor Post", content="Mentor content"
        )

    def test_anyone_can_list_discussions(self):
        url = reverse("discussion-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_unauthenticated_cannot_create_discussion(self):
        url = reverse("discussion-list")
        res = self.client.post(url, {"title": "Hi", "content": "Body"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_can_create_discussion_and_author_is_set(self):
        self.client.force_authenticate(user=self.learner)
        url = reverse("discussion-list")
        res = self.client.post(url, {"title": "New", "content": "Body"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["author"], "learner")

    def test_learner_can_update_own_discussion(self):
        self.client.force_authenticate(user=self.learner)
        url = reverse("discussion-detail", args=[self.learner_discussion.id])
        res = self.client.patch(url, {"title": "Updated"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_learner_cannot_update_others_discussion(self):
        self.client.force_authenticate(user=self.learner)
        url = reverse("discussion-detail", args=[self.other_discussion.id])
        res = self.client.patch(url, {"title": "Hack"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_mentor_can_update_any_discussion(self):
        self.client.force_authenticate(user=self.mentor)
        url = reverse("discussion-detail", args=[self.learner_discussion.id])
        res = self.client.patch(url, {"title": "Mentor edit"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_mentor_cannot_delete_discussion(self):
        self.client.force_authenticate(user=self.mentor)
        url = reverse("discussion-detail", args=[self.learner_discussion.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_any_discussion(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("discussion-detail", args=[self.learner_discussion.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class CommentAPITests(APITestCase):
    def setUp(self):
        self.learner = User.objects.create_user(
            username="learner", password="Pass12345", role="learner"
        )
        self.admin = User.objects.create_user(
            username="admin", password="Pass12345", role="admin"
        )

        self.discussion = Discussion.objects.create(
            author=self.learner, title="Topic", content="Content"
        )

        self.comment = Comment.objects.create(
            author=self.learner, discussion=self.discussion, content="Hello"
        )

    def test_anyone_can_view_discussion_comments(self):
        url = reverse("discussion-comments", args=[self.discussion.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_authenticated_can_post_comment_to_discussion(self):
        self.client.force_authenticate(user=self.learner)
        url = reverse("discussion-comments", args=[self.discussion.id])
        res = self.client.post(url, {"content": "New comment"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_unauthenticated_cannot_post_comment(self):
        url = reverse("discussion-comments", args=[self.discussion.id])
        res = self.client.post(url, {"content": "Nope"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_can_delete_any_comment(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("comment-detail", args=[self.comment.id])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
