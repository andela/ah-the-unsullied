import os
from rest_framework.views import status

# local imports
from .base_test import TestBase


class TestSocialAuth(TestBase):
    """This class has tests social auth."""

    def test_invalid_token(self):
        """Test response when token is invalid"""
        data = self.invalid_token
        url = self.social_auth_url
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_provider(self):
        """Test response when user uses an invalid provider"""
        data = self.invalid_provider
        url = self.social_auth_url
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_twitter(self):
        """Test login/signup using twitter keys"""
        url = self.social_auth_url
        data = {
            "provider": "twitter",
            "access_token": os.getenv('ACCESS_TOKEN'),
            "access_token_secret": os.getenv('SECRET_TOKEN')
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
