from rest_framework.test import APITestCase
from . import models
from comments.models import Comment
from users.models import User


class TestComments(APITestCase):
    COMM = "Comment COMM"
    URL = "/api/v1/texts/1/comments"

    def setUp(self):
        user = User.objects.create(username="test_user")
        Comment.objects.create(comment=self.COMM, user=user)

    def test_all_comments(self):
        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 200, "Status code isn't 200.")
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["comment"], self.COMM)
