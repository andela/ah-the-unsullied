import jwt
import json
from django.conf import settings
from rest_framework.views import status
from django.urls import reverse
from ..apps.articles.models import User, Article
# local imports
from .base_test import TestBase


class TestBookmarkArticle(TestBase):
    def add_article(self):
        # register user
        res = self.register_user()
        self.client.get(self.get_verify_url(self.user_data))
        # login user
        res = self.login_user()
        decoded = jwt.decode(res.data['token'], settings.SECRET_KEY,
                             algorithm='HS256')
        user = User.objects.get(email=decoded['email'])
        self.article = Article.objects.create(author_id=user.id,
                                              title='kenya moja',
                                              description='awesome',
                                              body='iko sawa')
        return res

    def add_new_user(self):
        user_data = {
            "user": {
                "username": "kelvin",
                "email": "kelvin@gmail.com",
                "password": "A23DVFRss@"
            }}
        login_data = {
            "user": {
                "email": "kelvin@gmail.com",
                "password": "A23DVFRss@"
            }}

        # register user
        self.client.post(
            self.user_url,
            user_data,
            format='json'
        )

        # activate user
        self.client.get(self.get_verify_url(user_data))

        # login user
        res = self.client.post(
            self.login_url,
            login_data,
            format="json"
        )
        return res

    def test_report_own_article(self):
        """Test if user can report their own an article"""
        slug = self.create_article().data['slug']
        res = self.login_user()
        response = self.client.post(
            reverse('articles:report_article',
                    kwargs={'slug': slug}
                    ),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + res.data['token'])

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'],
                         'You cannot report your own article.')

    def test_report_unavailable_article(self):
        """Test if user can report unavailable article"""
        res = self.add_new_user()
        response = self.client.post(
            reverse('articles:report_article',
                    kwargs={'slug': 'kenya-moja'}
                    ),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' +
                               res.data['token'])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], 'Article not found')

    def test_get_all_user_reported_articles(self):
        """Test if user can get all bookmarked articles"""
        res = self.add_article()
        response = self.client.get(
            reverse('articles:reported_articles'),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + res.data['token'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
