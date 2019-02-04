from rest_framework import status
from rest_framework.reverse import reverse

from .base_test import TestBase


class TestArticles(TestBase):

    def test_get_history(self):
        """This is the test for getting edited comments."""

        res = self.edit_comment()
        url = self.edit_history_url(res[0], res[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_history_of_non_existing_comment(self):
        """This is the test for non existing comment."""

        res = self.edit_comment()
        url = self.edit_history_url(res[0], 45)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['detail'],
            "This comment does not exist."
        )

    def test_get_history_with_non_integer(self):
        """This is the test for non integer."""

        res = self.edit_comment()
        url = self.edit_history_url(res[0], "jj")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['detail'],
            "Provide integer value for comment id."
        )

    def test_get_history_of_non_existing_article(self):
        """This is the test for non existing article."""

        res = self.edit_comment()
        url = self.edit_history_url(1, res[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "Article not found")

    def test_get_history_of_unedited(self):
        """This is the test for unedited comment."""

        slug = self.create_article().data['slug']
        url = reverse("articles:comment", kwargs={"slug": slug})
        res = self.client.post(url, self.comment_data, format="json")
        url = self.edit_history_url(slug, res.data['id'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, [])
