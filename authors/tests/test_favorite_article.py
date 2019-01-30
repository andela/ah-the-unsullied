import jwt
from django.conf import settings
from rest_framework.views import status
from django.urls import reverse
from ..apps.articles.models import User, Article
# local imports
from .base_test import TestBase


class TestFavoriteArticle(TestBase):

    def add_article(self):
        # register user
        self.register_user()
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

    def test_make_article_favorite(self):
        """Test if user can favorite an article"""
        res = self.add_article()
        response = self.client.put(
            reverse('articles:favorite_article',
                    kwargs={'slug': 'kenya-moja'}
                    ), content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + res.data['token'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"],
                         'Article successfully added to favorites')

    def test_add_unavailable_article_to_favorite(self):
        """Test if user can add unavailable article to favorites"""
        res = self.add_article()

        response = self.client.put(
            reverse('articles:favorite_article',
                    kwargs={'slug': 'kenya-mojaa'}
                    ), content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + res.data['token'])

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], 'Article not found')

    def test_remove_article_from_favorite(self):
        """Test if user can remove article from favorites"""
        res = self.add_article()

        self.client.put(
            reverse('articles:favorite_article',
                    kwargs={'slug': 'kenya-moja'}
                    ), content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + res.data['token'])

        response = self.client.put(
            reverse('articles:favorite_article', kwargs={'slug': 'kenya-moja'}
                    ), content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + res.data['token'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            'You have successfully removed this article from favorites')

    def test_get_all_favorite_articles(self):
        """Test if user can get all favorite articles"""
        res = self.add_article()

        response = self.client.get(
            reverse('articles:all_favourite_article'),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer ' + res.data['token'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
