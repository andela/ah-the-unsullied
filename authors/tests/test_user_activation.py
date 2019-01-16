# python and django imports
from rest_framework.views import status
from django.core import mail
from django.urls import reverse
from ..apps.authentication.models import User


# local imports
from .base_test import TestBase


class TestActivation(TestBase):
    """"This class has tests for email verification test case."""

    def test_email_sent_successfully(self):
        """"This is the test for a mail that was successfully sent"""

        response = self.register_user()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)

    def test_email_verification(self):
        """"This is the test for verified user"""

        response = self.client.get(self.get_verify_url(self.user_data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        message = 'Hey sam your account has been successfully activated '
        self.assertEqual(response.data, message)

    def test_invalid_link(self):
        """This is the test for an invalid link."""
        self.register_user()
        url = reverse('authentication:activate',
                      kwargs={"pk": 89, "token": 999999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'The link is invalid')

    def test_if_verified(self):
        self.client.get(self.get_verify_url(self.user_data))
        user = User.objects.get(username=self.user_data['user']['username'])
        self.assertEqual(user.is_verified, True)
