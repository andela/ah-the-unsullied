# python and django imports
import json
from rest_framework.views import status

# local imports
from .base_test import TestBase


class TestLogin(TestBase):
    """This class has tests for login test case."""

    def test_login(self):
        """This is the test for login with correct login details."""

        # register user
        self.client.post(
            self.user_url,
            self.user_data,
            format='json'
        )
        response = self.client.post(
            self.login_url,
            self.login_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wrong_login_details(self):
        """This is the test for login with wrong login details."""

        # register user
        self.client.post(
            self.user_url,
            self.user_data,
            format='json'
        )
        response = self.client.post(
            self.login_url,
            self.test_wrong_login,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content)['errors']['error'][0],
            'A user with this email and password was not found.'
             )

    def test_empty_email_login(self):
        """This is the test for login with empty email."""

        response = self.client.post(
            self.login_url,
            self.test_empty_email,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content)['errors']['email'][0],
            'This field may not be blank.'
        )
