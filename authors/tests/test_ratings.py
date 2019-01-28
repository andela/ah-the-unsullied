"""
Rate articles test module
"""
import json

from django.urls import reverse
from rest_framework.views import status

from .base_test import TestBase
from ..apps.ratings.responses import error_messages, success_messages


class RateArticleTestCase(TestBase):
    """
    Rate articles tests class
    """

    def test_rate_article(self):
        """
        test article is rated successfully
        """
        self.create_article()
        token = self.authentication_token_2()
        self.client.get(self.get_verify_url(self.user_data2))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(reverse('ratings:article_rating',
                                            kwargs={"slug": "another-post"}),
                                    self.rating,
                                    format="json"
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(3, json.loads(response.content)['data']["rating"])

    def test_author_cannot_rate_their_article(self):
        """
        Tests that the author cannot rate their own article
        """
        self.create_article()
        self.client.get(self.get_verify_url(self.user_data))
        response = self.client.post(reverse('ratings:article_rating',
                                            kwargs={"slug": "another-post"}),
                                    self.rating,
                                    format="json"
                                    )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(error_messages['unauthorized'],
                         response.data)

    def test_rating_non_existing_article(self):
        """
        Tests rating a non-existing article
        """
        self.create_article()
        token = self.authentication_token_2()
        self.client.get(self.get_verify_url(self.user_data2))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(reverse('ratings:article_rating',
                                            kwargs={"slug": "another"}),
                                    self.rating,
                                    format="json"
                                    )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(error_messages['not_exist'],
                         response.data)

    def test_article_with_invalid_rating(self):
        """
        Tests article rating is between 1-5
        """
        self.create_article()
        token = self.authentication_token_2()
        self.client.get(self.get_verify_url(self.user_data2))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(reverse('ratings:article_rating',
                                            kwargs={"slug": "another-post"}),
                                    self.wrong_rating,
                                    format="json"
                                    )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(error_messages['maximum_rating'],
                         response.data['errors']['rating'][0])

    def test_get_average_rating(self):
        """
        Tests that we get average rating of an article
        """
        # rate first time
        self.test_rate_article()

        # rate second time
        token = self.authentication_token_3()
        self.client.get(self.get_verify_url(self.user_data3))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(reverse('ratings:article_rating',
                                            kwargs={"slug": "another-post"}),
                                    self.another_rating,
                                    format="json"
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(4, json.loads(response.content)['data']["rating"])

        # test successful get of average rating
        response = self.client.get(self.article_url.format('another-post'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            3.5, json.loads(response.content)[
                'articles']['results'][0]['rating']
        )

    def test_update_rating(self):
        """
        tests that rating is updated when user submits a new rating
        """
        # rate article for the first time
        self.test_rate_article()

        # rate article for the second time
        response = self.client.post(reverse('ratings:article_rating',
                                            kwargs={"slug": "another-post"}),
                                    self.another_rating,
                                    format="json"
                                    )
        # assert that rating is updated
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(4, json.loads(response.content)['data']["rating"])

    def test_get_ratings_of_article_with_no_ratings(self):
        """
        Tests that an error message is returned when we try getting ratings
        for an article with no ratings
        """
        # create an article
        self.create_article()

        # login a user
        token = self.authentication_token_2()
        self.client.get(self.get_verify_url(self.user_data2))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # try to get ratings for the article
        response = self.client.get(reverse('ratings:article_rating',
                                           kwargs={"slug": "another-post"}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(error_messages['not_rated'],
                         json.loads(response.content)['detail'])

    def test_get_ratings_authenticated_user(self):
        """
        Tests that an authenticated user can get their ratings
        """
        # rate article for the first time
        self.test_rate_article()

        # get ratings
        response = self.client.get(reverse('ratings:article_rating',
                                           kwargs={"slug": "another-post"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['data'],
                         success_messages['data'])
        self.assertEqual(json.loads(response.content)['message'],
                         success_messages['message'])

    def test_average_rating_of_unrated_article_is_zero(self):
        """
        Tests that the average rating of an unrated article is zero
        """
        # create the article
        self.create_article()

        # get the article
        response = self.client.get(self.article_url.format('another-post'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content)['articles']['results'][0]['rating'], 0
        )

    def test_get_ratings_unauthenticated_user(self):
        """
        Tests that unauthenticated users see average rating
        """
        # create the article
        self.create_article()

        # try to get ratings for the article
        response = self.unauthenticated_client.get(
            reverse('ratings:article_rating',
                    kwargs={"slug": "another-post"})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['article'], 'another-post')
        self.assertEqual(response.data['average_rating'], 0)
        self.assertEqual(
            response.data['rating'], 'Please login to rate an article'
        )

    def test_get_ratings_of_inexistent_article(self):
        """
        Tests that getting ratings of an article that
        does not exist returns an error
        """
        # login a verified user
        token = self.authentication_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        self.client.get(self.get_verify_url(self.user_data))

        # try to get ratings of inexistent article
        response = self.client.get(reverse('ratings:article_rating',
                                           kwargs={"slug": "another-post"}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(error_messages['not_exist'], response.data)
