import jwt
import json
from django.conf import settings
from rest_framework.views import status
from django.urls import reverse
from ..apps.articles.models import User, Article
# local imports
from .base_test import TestBase


class TestBookmarkArticle(TestBase):

    def test_bookmark_article(self):
        """Test if user can bookmark an article"""
        token = self.authentication_token()
        response = self.create_bookmark_article(token)
        slug = response.data['slug']
        response = self.client.post(
            reverse('articles:bookmark_article',
                    kwargs={'slug': slug}
                    ), content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"],
                         'You have successfully bookmarked this article')

    def test_bookmark_unavailable_article(self):
        """Test if user can bookmark unavailable article"""
        self.create_article()
        res = self.login_user()
        response = self.client.post(
            reverse('articles:bookmark_article',
                    kwargs={'slug': 'kenya-mojaa'}
                    ), content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + res.data['token'])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], 'Article not found')

    def test_remove_article_from_bookmarks(self):
        """Test if user can remove article from bookmarks"""
        token = self.authentication_token()
        response = self.create_bookmark_article(token)
        slug = response.data['slug']
        self.client.post(
            reverse('articles:bookmark_article',
                    kwargs={'slug': slug}
                    ), content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(
            reverse('articles:bookmark_article',
                    kwargs={'slug': slug}
                    ), content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            'You have successfully removed this article from your bookmarks')

    def test_get_all_bookmarked_articles(self):
        """Test if user can get all bookmarked articles"""
        self.create_article()
        res = self.login_user()
        response = self.client.get(
            reverse('articles:bookmarked_articles'
                    ), content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + res.data['token'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
