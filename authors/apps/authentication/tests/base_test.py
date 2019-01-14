# django imports
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class TestBase(APITestCase):
    """This class defines the basic setup for the tests
        and the dummy data used for the tests.
    """

    def setUp(self):
        """This method is used to initialize variables used by the tests."""

        self.client = APIClient()
        self.login_url = reverse('authentication:login_url')
        self.user_url = reverse('authentication:signup_url')

        self.user_data = {
            "user": {
                "username": "sam",
                "email": "sam@gmail.com",
                "password": "A23DVFRss@"
            }}

        self.test_username = {
            "user": {
                "username": "sam",
                "email": "sam@gmail.com",
                "password": "A23DVFRss@"
            }}

        self.test_username2 = {
            "user": {
                "username": "sam",
                "email": "sly@gmail.com",
                "password": "A23DVFRss@"
            }}

        self.empty_email = {
            "user": {
                "username": "sam",
                "email": "",
                "password": "A23DVFRss@"
            }}

        self.empty_password = {
            "user": {
                "username": "sam",
                "email": "sami@gmail.com",
                "password": ""
            }}

        self.empty_username = {
            "user": {
                "username": "",
                "email": "sami@gmail.com",
                "password": "904438283278"
            }}

        self.login_data = {
            "user": {
                "email": "sam@gmail.com",
                "password": "A23DVFRss@"
            }}

        self.test_wrong_login = {
            "user": {
                "email": "sammy@gmail.com",
                "password": "A23DVFRss@"
            }}

        self.test_empty_email = {
            "user": {
                "email": "",
                "password": "A23@"
            }}

        self.test_login_unregistered = {
            "user": {
                "email": "sammy@gmail.com",
                "password": "A23@"
            }}
