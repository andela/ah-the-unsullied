"""
Module to test if token is returned during login_url/registration
"""
from rest_framework import status
import json


# local imports
from .base_test import TestBase


class TestTokenGeneration(TestBase):
    """ Test user registration/login_url returns token """

    def test_token_gen_on_signup(self):
        """
        Test if a token is returned after registration
        """
        response = self.client.post(
            self.user_url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # assert token is in the response
        self.assertIn('token', response.data)

    def test_login_url_returns_token(self):
        """
        Test if token is returned after login_url
        """
        self.client.post(
            self.login_url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        self.client.get(self.get_verify_url(self.user_data))
        response = self.client.post(
            self.login_url,
            data=json.dumps(self.login_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert token is in the response
        self.assertIn('token', response.data)
