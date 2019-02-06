from django.urls import reverse
from rest_framework import status
import json

from .base_test import TestBase


class TestCommentArticle(TestBase):
    """Tests for the user profile"""

    def test_highlight_article(self):
        slug = self.create_article().data['slug']
        url = reverse("articles:highlight", kwargs={"slug": slug})
        response = self.client.post(url, self.highlight_index, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_highlight_comments(self):
        url = self.single_highlight_comment_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_larger_than_end_index(self):
        slug = self.create_article().data['slug']
        url = reverse("articles:highlight", kwargs={"slug": slug})
        response = self.client.post(
            url, self.highlight_larger_start_index, format="json")
        self.assertEquals(
            response.data['message'], "The begin index should be less than the end index")

    def test_non_integer_index(self):
        slug = self.create_article().data['slug']
        url = reverse("articles:highlight", kwargs={"slug": slug})
        response = self.client.post(
            url, self.highlight_non_integer_index, format="json")
        self.assertEquals(response.data['error'],
                          "Please enter integer values only")

    def test_highlight_on_non_existant_article(self):
        self.verify_user()
        url = reverse("articles:highlight", kwargs={"slug": "slug"})
        response = self.client.post(
            url, self.highlight_non_integer_index, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.data['detail'], "Not found.")

    def test_get_highlight_comments(self):
        slug = self.create_article().data['slug']
        url = reverse("articles:highlight", kwargs={"slug": slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_highlight_comments_non_existant_article(self):
        self.verify_user()
        url = reverse("articles:highlight", kwargs={"slug": "slug"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.data['error'], "Article doesn't exist")

    def test_get_single_highlight_comments_non_existant_article(self):
        url = self.single_highlight_comment_non_existant_article_url()
        response = self.client.get(url)
        self.assertEquals(response.data['error'], "Article doesn't exist")

    def test_get_single_non_existant_highlight_comments(self):
        url = self.single_nonexistant_highlight_comment_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.data['error'],
                          "Highlight comment doesn't exist")

    def test_delete_single_highlight_comments(self):
        url = self.single_highlight_comment_url()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['message'],
                          "Highlight Comment deleted successfully")

    def test_delete_single_highlight_comments_non_existant_article(self):
        url = self.single_highlight_comment_non_existant_article_url()
        response = self.client.delete(url)
        self.assertEquals(response.data['error'], "Article doesn't exist")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_single_non_existant_highlight_comments(self):
        url = self.single_nonexistant_highlight_comment_url()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.data['error'],
                          "Highlight comment doesn't exist")

    def test_update_single_highlight_comments(self):
        url = self.single_highlight_comment_url()
        response = self.client.get(url)
        response = self.client.put(
            url, self.update_highlight_index, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_single_highlight_comments_non_existant_article(self):
        url = self.single_highlight_comment_non_existant_article_url()
        response = self.client.get(url)
        response = self.client.put(
            url, self.update_highlight_index, format='json')
        self.assertEquals(response.data['error'], "Article doesn't exist")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_single_non_existant_highlight_comments(self):
        url = self.single_nonexistant_highlight_comment_url()
        response = self.client.get(url)
        response = self.client.put(
            url, self.update_highlight_index, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.data['message'],
                          "Highlight comment does not exist")
