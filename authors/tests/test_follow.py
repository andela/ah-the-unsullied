from rest_framework.reverse import reverse
from rest_framework.views import status

# local imports
from .base_test import TestBase
from authors.apps.profiles.models import UserProfile


class TestFollow(TestBase):

    def test_follow_yourself(self):
        """Test handles a case where the user tries to follow themselves"""
        token = self.authentication_token()
        url = reverse('profiles:profile_details', kwargs={'username': 'sam'})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        self.client.get(url)
        follow_url = reverse('profiles:follow', kwargs={'username': 'sam'})
        response = self.client.post(follow_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_un_follow(self):
        """Test handles when a user un-follow a user"""
        self.follow()
        follow_url = reverse('profiles:follow', kwargs={'username': 'abdi'})
        response = self.client.post(follow_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow(self):
        """ Test handles when a user follows another """
        response = self.follow()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_following_list(self):
        """Test to handle a list of all users they are following"""
        self.follow()
        follow_list_url = reverse('profiles:following', kwargs={
            'username': 'sam'})
        response = self.client.get(follow_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follower_list(self):
        """ Test handles the request for all the  users followers"""
        self.follow()
        follower_list_url = reverse('profiles:follower', kwargs={
            'username': 'sam'})
        response = self.client.get(follower_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_model_check_if_following_method(self):
        """ Test if the model method to check if following works"""
        self.follow()
        profile = UserProfile.objects.get(user__username='abdi')
        user_to_check = UserProfile.objects.get(user__username='sam')
        following_status = user_to_check.check_if_following(profile)
        self.assertEqual(following_status, True)

    def test_model_toggle_method(self):
        """ Test the model toggle method to follow and un-follow """
        self.follow()
        profile = UserProfile.objects.get(user__username='abdi')
        user_to_check = UserProfile.objects.get(user__username='sam')
        user_to_check.toggle_follow(profile.user)
        following_status = user_to_check.check_if_following(profile)
        self.assertEqual(following_status, False)
        user_to_check.toggle_follow(profile.user)
        following_status = user_to_check.check_if_following(profile)
        self.assertEqual(following_status, True)
