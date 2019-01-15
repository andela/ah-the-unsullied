"""
Module to test if token is returned during login_url/registration
"""
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
import json


# initialize the APIClient app
client = Client()


class TestTokenGeneration(TestCase):
    """ Test user registration/login_url returns token """

    def setUp(self):
        self.user_data = {
            'user': {
                'username': 'Allan123',
                'email': 'cake@foo.com',
                'password': 'Yertg234D#'
            }
        }

    def test_token_gen_on_signup(self):
        """
        Test if a token is returned after registration
        """
        response = client.post(
            reverse('authentication:signup_url'),
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
        client.post(
            reverse('authentication:signup_url'),
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        response = client.post(
            reverse('authentication:login_url'),
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert token is in the response
        self.assertIn('token', response.data)
