from django.urls import reverse
from rest_framework import status
import json

from .base_test import TestBase


class TestCommentArticle(TestBase):
    """Tests for the user profile"""

    def test_add_comment(self):
        url = self.get_comment_url()
        response = self.client.post(url, self.comment_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_comments(self):
        url = self.get_comment_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_threads(self):
        url = self.get_child_comment_url()
        response = self.client.post(url, self.thread_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def get_nonexistant_comment_url(self):
        response = self.comment_on_nonexistant_comment()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['error'], "Comment not found.")

    def test_get_child_comment(self):
        url = self.get_child_comment_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistant_comments(self):
        get_url = self.get_nonexistant_child_comment_url()
        response = self.client.get(get_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "comment doesn't exist")

    def test_delete_nonexistant_comments(self):
        get_url = self.get_nonexistant_child_comment_url()
        response = self.client.delete(get_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "comment doesn't exist")

    def test_update_child_comment(self):
        url = self.get_child_comment_url()
        self.client.get(url)
        response = self.client.put(url, self.update_child_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_child_comment(self):
        url = self.get_child_comment_url()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         "Comment deleted successfully")
   
    def test_update_nonexistant_comments(self):
        get_url = self.get_nonexistant_child_comment_url()
        response = self.client.put(get_url, self.update_child_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], "Comment does not exist")

    def test_get_comment_on_non_existant_article(self):
        comment_url = reverse("articles:comment", kwargs={"slug": "slug"})
        response = self.client.get(
            comment_url, self.comment_data, format="json")
        self.assertEquals(response.data['error'], "Article doesn't exist")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_comment_on_non_existant_article(self):
        self.verify_user()
        comment_url = reverse("articles:comment", kwargs={"slug": "slug"})
        response = self.client.post(
            comment_url, self.comment_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment_on_non_existant_article(self):
        self.verify_user()
        comment_url = reverse("articles:thread", kwargs={"slug": "slug", "id": 4})
        response = self.client.delete(comment_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.data['error'], "Article doesn't exist")
