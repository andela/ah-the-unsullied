import json
from rest_framework.views import status
from django.urls import reverse
from authors.apps.articles.response_messages import error_messages, \
    success_messages

# local imports
from .base_test import TestBase


class TestArticles(TestBase):

    def test_create_valid_article(self):
        """ Test create an article with valid data """
        token = self.authentication_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        self.client.get(self.get_verify_url(self.user_data))
        response = self.client.post(
            self.article_url,
            data=json.dumps(self.valid_article_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_article_unverified_user(self):
        """ Test create an article with valid data """
        self.create_article()
        token = self.authentication_token_2()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(
            self.article_url,
            data=json.dumps(self.valid_article_data),
            content_type='application/json'
        )
        self.assertIn(response.data, error_messages['email_verification'])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_invalid_article(self):
        """ Test create an article with invalid data """
        token = self.authentication_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        self.client.get(self.get_verify_url(self.user_data))
        response = self.client.post(
            self.article_url,
            data=json.dumps(self.invalid_article_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_article_unauthorized(self):
        """ Test create an article as an unauthorized  user"""
        self.client.get(self.get_verify_url(self.user_data))
        response = self.client.post(
            self.article_url,
            data=json.dumps(self.invalid_article_data),
            content_type='application/json'
        )
        self.assertIn(error_messages['authentication'],
                      response.data['detail'])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_articles(self):
        """Test to get all articles """
        self.create_article()
        self.client.get(self.get_verify_url(self.user_data))
        response = self.client.get(
            self.article_url,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_get(self):
        response = self.client.get(
            self.article_url,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_article(self):
        """Test to get a single article """
        self.create_article()
        self.client.get(self.get_verify_url(self.user_data))
        response = self.client.get(
            reverse(
                'articles:detail_article',
                kwargs={'slug': 'another-post'}
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_single_article(self):
        """Test to get a nonexistent article """
        self.create_article()
        self.client.get(self.get_verify_url(self.user_data))
        response = self.client.get(
            reverse(
                'articles:detail_article',
                kwargs={'slug': 'another-posts'}
            ),
            content_type='application/json'
        )
        self.assertEqual(error_messages['article_404'], response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_article(self):
        """Test updating an article """
        self.create_article()
        self.client.get(self.get_verify_url(self.user_data))
        response = self.client.put(
            reverse(
                'articles:detail_article',
                kwargs={'slug': 'another-post'},
            ),
            data=json.dumps(self.invalid_article_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_nonexistent_article(self):
        """Test updating a nonexistent article """
        self.create_article()
        self.client.get(self.get_verify_url(self.user_data))
        response = self.client.put(
            reverse(
                'articles:detail_article',
                kwargs={'slug': 'another-posts'},
            ),
            data=json.dumps(self.invalid_article_data),
            content_type='application/json'
        )
        self.assertIn(error_messages['article_404'], response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_article(self):
        """Test deleting an article """
        self.create_article()
        self.client.get(self.get_verify_url(self.user_data))
        response = self.client.delete(
            reverse(
                'articles:detail_article',
                kwargs={'slug': 'another-post'},
            ),
            content_type='application/json'
        )
        self.assertIn(success_messages['deleted'], response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_nonexistent_article(self):
        """Test delete a non-existing article """
        self.create_article()
        self.client.get(self.get_verify_url(self.user_data))
        response = self.client.delete(
            reverse(
                'articles:detail_article',
                kwargs={'slug': 'another-posts'},
            ),
            content_type='application/json'
        )
        self.assertIn(error_messages['article_404'], response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_unauthorized(self):
        """Test delete with an unauthorized user"""
        response = self.client.delete(
            reverse(
                'articles:detail_article',
                kwargs={'slug': 'another-post'},
            ),
            content_type='application/json'
        )
        self.assertIn(error_messages['authentication'],
                      response.data['detail'])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_article_none_author(self):
        """ Test delete if article is not owner """
        self.create_article()
        token = self.authentication_token_2()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.delete(
            reverse(
                'articles:detail_article',
                kwargs={'slug': 'another-post'},
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn(response.data, error_messages['unauthorised'])

    def test_update_article_none_author(self):
        """ Test update if article is not owner """
        self.create_article()
        token = self.authentication_token_2()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.put(
            reverse(
                'articles:detail_article',
                kwargs={'slug': 'another-post'},
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn(response.data, error_messages['unauthorised'])

    def test_update_article_null_data(self):
        """Test updating an article with null inputs"""
        self.create_article()
        self.client.get(self.get_verify_url(self.user_data))
        response = self.client.put(
            reverse(
                'articles:detail_article',
                kwargs={'slug': 'another-post'},
            ),
            data=json.dumps(self.null_article_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(response.data, error_messages['null_update'])
