from django.urls import path
from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
)

""" Django 2.0 requires the app_name variable set when using include 
namespace
"""
app_name = 'authentication'

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='user_update'),
    path('users/', RegistrationAPIView.as_view(), name="signup_url"),
    path('users/login/', LoginAPIView.as_view(), name="login_url")
]
