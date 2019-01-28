from django.urls import path,include
from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
    PasswordReset, PasswordDone,
    ActivationLinkView, SocialAuth
)

""" Django 2.0 requires the app_name variable set when using include
namespace
"""
app_name = 'authentication'

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='user_update'),
    path('users/', RegistrationAPIView.as_view(), name="signup_url"),
    path('users/login/', LoginAPIView.as_view(), name="login_url"),
    path('social', SocialAuth.as_view(), name="social_auth"),
    path('activate/account/<str:pk>/<str:token>',
         ActivationLinkView.as_view(), name="activate"
         ),
    path('users/password-reset/', PasswordReset.as_view(),
         name="password_reset"),
    path('users/password-done/<str:token>', PasswordDone.as_view(),
         name="password_done"),
]
