# python and django imports
from django.urls import reverse
from rest_framework import status

# local imports
from .base_test import TestBase


class TestPagination(TestBase):
    """This class has tests for pagination setting."""

    def test_profiles_pagination(self):
        token = self.get_token()
        url = reverse('profiles:all_profiles')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(url)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('next_page', response.data['pages'])
        self.assertIn('previous_page', response.data['pages'])
