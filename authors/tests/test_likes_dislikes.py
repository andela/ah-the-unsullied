from rest_framework.reverse import reverse
from rest_framework.views import status

# local imports
from .base_test import TestBase


class TestLikesDislikes(TestBase):
    """This class has tests for like and dislike test case."""

    def test_like_article(self):
        """This is the test for like to an article."""

        slug = self.create_article().data['slug']
        url = reverse("articles:article-like-like", kwargs={"slug": slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['likes'], 1)

    def test_dislike_article(self):
        """This is the test for disliking an article."""

        slug = self.create_article().data['slug']
        url = reverse("articles:article-like-dislike", kwargs={"slug": slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['dislikes'], 1)

    def test_unlike_article(self):
        """This is the test for un-dislike to an article."""

        slug = self.create_article().data['slug']
        url = reverse("articles:article-like-dislike", kwargs={"slug": slug})
        self.client.post(url)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def like_dislike_article(self):
        """This is the test for changing like to dislike of an article."""

        slug = self.create_article().data['slug']
        url = reverse("articles:article-like-like", kwargs={"slug": slug})
        url2 = reverse("articles:article-like-dislike", kwargs={"slug": slug})
        self.client.post(url)
        response = self.client.post(url2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def dislike_like_article(self):
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

    def test_like_comment(self):
        """
        Tests that a comment on an article can be liked
        """
        # create an article and add a comment
        slug = self.create_article().data['slug']
        url = reverse("articles:comment", kwargs={"slug": slug})
        response = self.client.post(url, self.comment_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # like that comment
        comment_id = response.data['id']
        url = reverse("articles:like-comment", kwargs={
            "comment_id": comment_id, "slug": slug
        }
                      )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['likes_on_comment'], 1)

    def test_unlike_comment(self):
        """
        Tests that a comment on an article can be unliked
        """
        # create an article and add a comment
        slug = self.create_article().data['slug']
        url = reverse("articles:comment", kwargs={"slug": slug})
        response = self.client.post(url, self.comment_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # like that comment
        comment_id = response.data['id']
        url = reverse("articles:like-comment",
                      kwargs={"comment_id": comment_id, "slug": slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['likes_on_comment'], 1)

        # unlike comment
        url = reverse("articles:like-comment",
                      kwargs={"comment_id": comment_id, "slug": slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['likes_on_comment'], 0)

    def test_dislike_comment(self):
        """
        Tests that a comment can be disliked
        """
        # create an article and add a comment
        slug = self.create_article().data['slug']
        url = reverse("articles:comment", kwargs={"slug": slug})
        response = self.client.post(url, self.comment_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # dislike the comment
        comment_id = response.data['id']
        url = reverse("articles:dislike-comment",
                      kwargs={"comment_id": comment_id, "slug": slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['dislikes_on_comment'], 1)

    def test_un_dislike_dislike(self):
        """
        Tests that a user can undislike dislike
        """
        # create the article and add a comment
        slug = self.create_article().data['slug']
        url = reverse("articles:comment", kwargs={"slug": slug})
        response = self.client.post(url, self.comment_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # dislike the comment
        comment_id = response.data['id']
        url = reverse("articles:dislike-comment",
                      kwargs={"comment_id": comment_id, "slug": slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['dislikes_on_comment'], 1)

        # dislike the comment
        url = reverse("articles:dislike-comment",
                      kwargs={"comment_id": comment_id, "slug": slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['dislikes_on_comment'], 0)

    def test_dislike_then_like_comment(self):
        """
        Tests that a comment can be disliked then liked
        """
        # create an article and add a comment
        slug = self.create_article().data['slug']
        url = reverse("articles:comment", kwargs={"slug": slug})
        response = self.client.post(url, self.comment_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # dislike the comment
        comment_id = response.data['id']
        url = reverse("articles:dislike-comment",
                      kwargs={"comment_id": comment_id, "slug": slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['dislikes_on_comment'], 1)

        # like that comment
        url = reverse("articles:like-comment",
                      kwargs={"comment_id":  comment_id, "slug": slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['likes_on_comment'], 1)
        self.assertEqual(response.data['dislikes_on_comment'], 0)

    def test_like_dislike_comment(self):
        """
        Tests that a comment can be liked then disliked
        """
        # create an article and add a comment
        slug = self.create_article().data['slug']
        url = reverse("articles:comment", kwargs={"slug": slug})
        response = self.client.post(url, self.comment_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # like the comment
        comment_id = response.data['id']
        url = reverse("articles:like-comment",
                      kwargs={"comment_id": comment_id, "slug": slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['likes_on_comment'], 1)

        # dislike the comment
        url = reverse("articles:dislike-comment",
                      kwargs={"comment_id": comment_id, "slug": slug}
                      )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['dislikes_on_comment'], 1)
        self.assertEqual(response.data['likes_on_comment'], 0)

    def test_get_all_likes_dislikes_comment(self):
        """
        Tests that we can get all likes and dislikes for a comment
        """
        # create the comment
        slug = self.create_article().data['slug']
        url = reverse("articles:comment", kwargs={"slug": slug})
        response = self.client.post(url, self.comment_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # like the comment
        comment_id = response.data['id']
        url = reverse("articles:like-comment",
                      kwargs={"comment_id": comment_id, "slug": slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['likes_on_comment'], 1)
        self.assertEqual(response.data['dislikes_on_comment'], 0)
