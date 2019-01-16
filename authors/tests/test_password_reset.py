"""
Module to test password reset view
"""
import os
from datetime import datetime, timedelta

import jwt
from django.test import Client
from django.urls import reverse
from rest_framework import status

from .base_test import TestBase
import json

# initialize the APIClient app
client = Client()


class TestPasswordReset(TestBase):
    """ Test user password reset """

    def test_email_sent_to_user_on_reset(self):
        """
        Test if an email  will be sent to the
        user's email account on reset
        """
        self.register_user()
        response = client.post(
            reverse('authentication:password_reset'),
            data=json.dumps(self.reset_password_email),
            content_type='application/json'
        )
        self.assertEqual(response.data['message'],
                         'Email sent successfully. '
                         'Find the password reset link in your email')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_inexistent_email_returns_error_message(self):
        """
        Tests that an error will be returned
        for an inexistent email
        """

        self.register_user()
        response = client.post(reverse('authentication:password_reset'),
                               data=json.dumps(self.inexistent_email),
                               content_type='application/json')
        self.assertEqual(response.data['message'],
                         'The Email provided is not registered')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_not_provided_by_user(self):
        """Tests the error returned when the user does not supply his email"""
        self.register_user()
        response = client.post(
            reverse('authentication:password_reset'),
            data=json.dumps(self.blank_mail),
            content_type='application/json'
        )
        self.assertEqual(response.data['errors']['email'][0],
                         'Please supply your email.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_password_successful(self):
        """
        Test password successfully reset
        """

        result = self.register_user()
        self.reset_password = {"password": "Aklklpha123#",
                               "confirm_password": "Aklklpha123#"}
        response = client.put(
            reverse('authentication:password_done',
                    kwargs={'token': result.data['token']}),
            data=json.dumps(self.reset_password),
            content_type='application/json'
        )
        self.assertEqual(response.data['message'],
                         'Password successfully updated')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_and_confirm_password_match(self):
        """
        Tests that the Password and Confirm Password fields match
        """
        result = self.register_user()
        self.reset_password = {"password": "Aklpha13#",
                               "confirm_password": "Aklklpha123#"}
        response = client.put(
            reverse('authentication:password_done',
                    kwargs={'token': result.data['token']}),
            data=json.dumps(self.reset_password),
            content_type='application/json'
        )
        self.assertEqual(response.data['message'], 'Passwords do not match')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_expired_token_raises_error(self):
        """
        Tests that using an expired token raises an error
        """
        self.register_user()
        self.reset_password = {"password": "Aklklpha123#",
                               "confirm_password": "Aklklpha123#"}
        token = jwt.encode({
            "email": "sam@gmail.com", "iat": datetime.now(),
            "exp": datetime.utcnow() - timedelta(seconds=1)},
            os.getenv('SECRET_KEY'), algorithm='HS256').decode()
        response = self.client.put(reverse('authentication:password_done',
                                           kwargs={
                                               'token': token}),
                                   data=json.dumps(self.reset_password),
                                   content_type='application/json')
        self.assertEqual(response.data['message'], 'The link has expired')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
