import pdb

from django.test import Client
from django.urls import reverse
from rest_framework.views import status

from .base_test import TestBase
from .test_profile import TestUserProfile

# initialize API Client
client = Client
profile = TestUserProfile


class RateArticleTestCase(TestBase):
    """
    Rate articles tests class
    :params: BaseTest:
      the base test class
    """

    def test_successful_article_creation(self):
        """
        Tests that the article is created successfully
        """
        token = self.authentication_token()
        response = self.client.post(self.articles_url, self.article_data,
                                    HTTP_AUTHORIZATION='Bearer ' + token,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual('new title', response.data["title"])
        return response

    def test_article_rating_successful(self):
        """
        Tests that an article is rated successfully
        """
        token = self.authentication_token_2()
        self.test_successful_article_creation()

        response = self.client.post(self.rate.format('new-title'),
                                    self.test_rating,
                                    HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(5, response.data["rating"])

    def test_author_cannot_rate_their_article(self):
        """
        Tests that an author cannot rate their article
        """
        token = self.authentication_token()
        response = self.client.post(self.articles_url, self.article_data,
                                    HTTP_AUTHORIZATION='Bearer ' + token,
                                    format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.rate.format('new-title'),
                                    self.test_rating,
                                    HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('Error, you cannot rate your own article',
                         response.data['errors'][0])

    def test_inexistent_article(self):
        """
        Tests that an error is raised when trying to
        rate a non-existent article
        """
        token = self.authentication_token_2()
        self.test_successful_article_creation()
        response = self.client.post(self.rate.format('new-titl'),
                                    self.test_rating,
                                    HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('Error, Article does not exist',
                         response.data['errors'][0])

    def test_invalid_rating(self):
        """
        Tests that rating > 5 and less than 0 raises an error
        """
        token = self.authentication_token_2()
        self.test_successful_article_creation()
        response = self.client.post(self.rate.format('new-title'),
                                    self.invalid_rating,
                                    HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('Error, rating is between 1 to 5',
                         response.data['errors'][0])

    def test_get_average_rating(self):
        """
        Tests that we can get the average rating of an article
        """
        # first rating
        token = self.authentication_token_2()
        self.test_successful_article_creation()

        response = self.client.post(self.rate.format('new-title'),
                                    self.test_rating,
                                    HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(5, response.data["rating"])

        # second rating
        token = self.another_authentication_token()
        response = self.client.post(self.rate.format('new-title'),
                                    self.new_rating,
                                    HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(3, response.data["rating"])

        # third rating
        token = self.authentication_token_3()
        response = self.client.post(self.rate.format('new-title'),
                                    self.new_rating,
                                    HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(
            reverse('articles:detail_article',
                    kwargs={'slug': 'new-title'}
                    ),
            HTTP_AUTHORIZATION='Bearer ' + token
        )
        self.assertEqual(3.7, response.data["average_rating"])

    def test_unauthorized_user_cannot_rate_articles(self):
        """
        Tests that unauthorized users cannot rate articles
        """
        self.test_successful_article_creation()

        response = self.client.post(self.rate.format('new-title'),
                                    self.test_rating)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
