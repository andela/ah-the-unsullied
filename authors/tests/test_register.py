# python and Django imports
from rest_framework.views import status
import json

# local imports
from .base_test import TestBase


class TestRegister(TestBase):
    """This class has tests for user registration test case"""

    def test_register_user(self):
        """This is the test for register with correct data."""

        response = self.client.post(
            self.user_url,
            self.user_data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_duplicate_email(self):
        """This is the test for register with duplicate email."""

        # register user
        self.client.post(
            self.user_url,
            self.user_data,
            format='json'
            )
        response = self.client.post(
            self.user_url,
            self.user_data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content)['errors']['email'][0],
            'Email already exists. Please enter another email or sign in'
        )

    def test_register_duplicate_username(self):
        """This is the test for register with duplicate username."""

        # register user
        self.client.post(
            self.user_url,
            self.test_username,
            format='json'
            )
        response = self.client.post(
            self.user_url,
            self.test_username2,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_empty_email(self):
        """This is the test for register with empty email."""

        response = self.client.post(
            self.user_url,
            self.empty_email,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_empty_password(self):
        """This is the test for register with empty password."""

        response = self.client.post(
            self.user_url,
            self.empty_password,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_empty_username(self):
        """This is the test for register with empty username."""

        response = self.client.post(
            self.user_url,
            self.empty_username,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_update(self):
        """Test user update"""
        self.client.post(
            self.user_url,
            self.user_data,
            format='json'
            )
        self.client.get(self.get_verify_url(self.user_data))
        res = self.client.post(
                self.login_url,
                data=json.dumps(self.user_data),
                content_type='application/json'
            )
        token = res.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.put(
            self.update_url,
            self.update_data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_current_user(self):
        self.client.post(
            self.user_url,
            self.user_data,
            format='json'
            )
        self.client.get(self.get_verify_url(self.user_data))
        res = self.client.post(
                self.login_url,
                data=json.dumps(self.user_data),
                content_type='application/json'
            )
        token = res.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
