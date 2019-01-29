import json
import os
from rest_framework.views import status
from django.urls import reverse

# local imports
from .base_test import TestBase


class TestShareArticles(TestBase):

    def test_share_article_via_email(self):
        response = self.share_article_via_email()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Article successfully shared")

    def test_share_article_via_facebook(self):
        facebook_share_url = self.share_article_via_facebook()
        response = self.client.post(facebook_share_url)
        self.assertEqual(response.data['link'],
                         'https://www.facebook.com/sharer/sharer.php?u='
                         + self.base_url + 'api/articles/another-post')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_share_article_via_twitter(self):
        slug = self.create_article().data['slug']
        twitter_share_url = reverse(
            "articles:twitter_share", kwargs={"slug": slug})
        response = self.client.post(twitter_share_url)
        self.assertEqual(response.data['link'],
                         'https://twitter.com/home?status=The%20unsullied%20have%20shared%20'
                         + self.base_url + 'api/articles/another-post')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_share_nonexistant_article_via_email(self):
        self.verify_user()
        email_share_url = reverse(
            "articles:email_share", kwargs={"slug": "slug"})
        response = self.client.post(
            email_share_url, self.share_email_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Article not found")

    def test_share_nonexistant_article_via_facebook(self):
        self.verify_user()
        facebook_share_url = reverse(
            "articles:facebook_share",  kwargs={"slug": "slug"})
        response = self.client.post(facebook_share_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Article not found")

    def test_share_nonexistant_article_via_twitter(self):
        self.verify_user()
        twitter_share_url = reverse(
            "articles:twitter_share",  kwargs={"slug": "slug"})
        response = self.client.post(twitter_share_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Article not found")
