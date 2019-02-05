from django.urls import path

from .views import (ProfileListView, ProfileDetail, FollowingView, FollowList,
                    FollowerList)
"""
Django 2.0 requires the app_name variable set when using include namespace
"""
app_name = 'profiles'

urlpatterns = [
    path('', ProfileListView.as_view(), name='all_profiles'),
    path('<str:username>', ProfileDetail.as_view(), name='profile_details'),
    # follow/unfollow the username in url
    path('<str:username>/follow', FollowingView.as_view(), name='follow'),
    # users following username in the url
    path('<str:username>/following', FollowList.as_view(), name='following'),
    # users the username in the url follows
    path('<str:username>/followers', FollowerList.as_view(), name='follower')

]
