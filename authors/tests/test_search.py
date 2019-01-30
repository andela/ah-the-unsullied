import json
from rest_framework.views import status
from django.urls import reverse

# local imports
from .base_test import TestBase


class TestFilterSet(TestBase):

    def test_get_article_by_author(self):
        """test_get_article_by_author """
        self.verify_user()
        self.client.get(self.get_verify_url(self.user_data))
        self.client.post(
            self.article_url,
            data=json.dumps(self.valid_article_data),
            content_type='application/json'
        )
        url = reverse('search') + '?author = {}'.format('sam')
        response = self.client.get(
            url,
            content_type='application/json'
        )
        articles = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(articles), 1)

    def test_get_article_by_tag(self):
        """test_get_article_by_tag """
        self.verify_user()
        self.client.get(self.get_verify_url(self.user_data))
        self.client.post(
            self.article_url,
            data=json.dumps(self.valid_article_data),
            content_type='application/json'
        )
        url = reverse('search') + '?tagList = {}'.format('young')
        response = self.client.get(
            url,
            content_type='application/json'
        )
        articles = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(articles), 1)
