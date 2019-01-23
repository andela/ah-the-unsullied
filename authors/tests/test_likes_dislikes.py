from rest_framework.reverse import reverse
from rest_framework.views import status

# local imports
from .base_test import TestBase


class TestLikesDislikes(TestBase):
    """This class has tests for like and dislike test case."""

    def test_like(self):
        """This is the test for like to an article."""

        slug = self.create_article().data['slug']
        url = reverse("articles:article-like-like", kwargs={"slug": slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['likes'], 1)

    def test_dislike(self):
        """This is the test for dislike to an article."""

        slug = self.create_article().data['slug']
        url = reverse("articles:article-like-dislike", kwargs={"slug": slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['dislikes'], 1)

    def test_unlike(self):
        """This is the test for un-dislike to an article."""

        slug = self.create_article().data['slug']
        url = reverse("articles:article-like-dislike", kwargs={"slug": slug})
        self.client.post(url)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def like_dislike(self):
        """This is the test for changing like to dislike of an article."""

        slug = self.create_article().data['slug']
        url = reverse("articles:article-like-like", kwargs={"slug": slug})
        url2 = reverse("articles:article-like-dislike", kwargs={"slug": slug})
        self.client.post(url)
        response = self.client.post(url2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def dislike_like(self):
        """This is the test for changing dislike to like of an article."""
        slug = self.create_article().data['slug']
        url = reverse("articles:article-like-dislike",
                      kwargs={"slug": slug})
        url2 = reverse("articles:article-like-dislike",
                       kwargs={"slug": slug})
        self.client.post(url2)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['likes'], 1)

    def test_get_likes_dislike(self):
        """This is the test for getting likes and dislikes of an article."""
        slug = self.create_article().data['slug']
        url = reverse("articles:article-like-dislike", kwargs={"slug": slug})
        self.client.post(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['likes'], 0)
        self.assertEqual(response.data['dislikes'], 1)
