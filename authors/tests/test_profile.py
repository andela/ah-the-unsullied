from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import json


class TestUserProfile(APITestCase):
    """Tests for the user profile"""

    def setUp(self):
        """This method is used to initialize variables used by the tests."""
        self.client = APIClient()
        self.user_data = {
            "user": {
                "username": "sam",
                "email": "sam@gmail.com",
                "password": "A23DVFRss@"
            }}
        self.user_data2 = {
            "user": {
                "username": "catherine",
                "email": "catherine@gmail.com",
                "password": "A23DVFRss@"
            }}
        self.update_data = {
            "user": {
                "bio": "catherine"
            }}

    def get_token_on_signup(self,):
            return self.client.post(
                reverse('authentication:signup_url'),
                data=json.dumps(self.user_data),
                content_type='application/json'
            )

    def authentication_token(self,):
        res = self.get_token_on_signup()
        token = res.data['token']
        return token

    def test_create_profile(self):
        """Test create profile on registration """
        token = self.authentication_token()
        url = reverse('profiles:profile_details', kwargs={'username': 'sam'})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(url)
        self.assertEqual(response.data['username'], 'sam')

    def test_get_all_profiles(self):
        """Test for getting a all profiles"""
        token = self.authentication_token()
        url = reverse('profiles:all_profiles')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_profile_details(self):
        """Test for getting a single userprofile"""
        token = self.authentication_token()
        url = reverse('profiles:profile_details', kwargs={'username': 'sam'})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_profile_update(self):
        """Test profile update"""
        token = self.authentication_token()
        url = reverse('profiles:profile_details', kwargs={'username': 'sam'})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.put(url, data=json.dumps(self.update_data),
                                   content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_non_existing_profile(self):
        """Test for getting non existing profile"""
        token = self.authentication_token()
        url = reverse('profiles:profile_details', kwargs={'username': 'kwanj'})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_other_profile(self):
        """Tests for updating  another person's profile"""
        token = self.authentication_token()
        self.client.post(
                reverse('authentication:signup_url'),
                data=json.dumps(self.user_data2),
                content_type='application/json'
            )
        url = reverse('profiles:profile_details',kwargs={'username':'catherine'})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.put(url, data={
                                        "user": {
                                            "bio": "terrible"
                                        }
                                    },
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
