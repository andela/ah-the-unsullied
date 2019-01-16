from django.urls import path

from .views import ProfileListView, ProfileDetail
"""
Django 2.0 requires the app_name variable set when using include namespace
"""
app_name = 'profiles'

urlpatterns = [
    path('', ProfileListView.as_view(), name='all_profiles'),
    path('<str:username>', ProfileDetail.as_view(), name='profile_details')
]
