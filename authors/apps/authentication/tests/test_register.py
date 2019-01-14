# python and Django imports
from rest_framework.views import status

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
