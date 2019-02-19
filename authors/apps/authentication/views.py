import os
from builtins import BaseException

from datetime import datetime, timedelta

import jwt
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from jwt import ExpiredSignatureError
from rest_framework import status
from rest_framework.generics import (
    RetrieveUpdateAPIView, CreateAPIView, UpdateAPIView, ListAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_core.exceptions import MissingBackend

from .activate import account_activation_token
from .models import User
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    EmailCheckSerializer, PasswordResetSerializer, ActivateSerializer,
)
from .backends import get_jwt_token
activation_url = os.getenv('ACTIVATION_URL')


class RegistrationAPIView(CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        
        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # get the user by their username
        user_to_activate = User.objects.get(username=user['username'])

        # Get the email of the user
        to_email = user_to_activate.email

        # Encode the user id
        user_pk = user_to_activate.pk
        user_id = urlsafe_base64_encode(force_bytes(user_pk)).decode()

        # Generate the token
        token = account_activation_token.make_token(user_to_activate)

        # pass data to the reverse url
        url = "{}".format(
            reverse(
                'authentication:activate',
                kwargs={
                    'pk': user_id,
                    'token': token
                }
            ))

        # create activation link
        activation_link = "{scheme}://{host}{route}".format(
            scheme=request.scheme,
            host=activation_url,
            route=url
        )
        username = user_to_activate.username

        message = render_to_string(
            'activate.html', {
                'username': username,
                'link': activation_link
            })

        mail_subject = 'Activate your Authors Haven Account'

        send_mail(mail_subject, message, '', [to_email, ],
                  html_message=message, fail_silently=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ActivationLinkView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ActivateSerializer

    def get(self, request, **kwargs):

        try:
            # Get the arguments form the url
            encoded_user = kwargs.get('pk')
            token = kwargs.get('token')

            # Decode the user and query to get user
            user_id = urlsafe_base64_decode(encoded_user).decode()
            user = User.objects.get(pk=user_id)

        # If raise exception errors set to None
        except (ValueError, TypeError, User.DoesNotExist):
            user = None

        # Get the valid token
        matching_token = account_activation_token.check_token(
            user, token=token
        )
        # activate user if all is valid
        if user and matching_token is not None:
            user.is_verified = True
            user.save()
            return Response(
                'Hey {} your account has been successfully activated '
                ''.format(user.username),
                status.HTTP_201_CREATED
            )

        # Else show the link is invalid
        invalid_message = 'The link is invalid'
        return Response(invalid_message, status.HTTP_400_BAD_REQUEST)


class PasswordReset(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EmailCheckSerializer

    def post(self, request):
        email = request.data.get('email', {})
        serializer = self.serializer_class(data={"email": email})
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            message = {"message": "The Email provided is not registered"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        token = jwt.encode({
            "email": email, "iat": datetime.now(),
            "exp": datetime.utcnow() + timedelta(hours=1)},
            os.getenv('SECRET_KEY'), algorithm='HS256').decode()

        hosting = activation_url

        my_link = \
            'https://' + hosting + '/api/users/password-done/{}'.format(token)
        message = render_to_string(
            'reset_email.html', {
                'user': email,
                'domain': my_link,
                'token': token,
                'username': username,
                'link': my_link
            })

        send_mail('You requested password reset',
                  'Reset your password', '', [email, ], html_message=message,
                  fail_silently=False)
        return Response({"message": "Email sent successfully. "
                                    "Find the password reset link in your "
                                    "email"},
                        status=status.HTTP_200_OK)


class PasswordDone(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = PasswordResetSerializer
    lookup_url_kwarg = 'token'

    def put(self, request, **kwargs):
        token = self.kwargs.get(self.lookup_url_kwarg)
        try:
            decoded_token = jwt.decode(token, os.getenv('SECRET_KEY'),
                                       algorithm='HS256')
            email = decoded_token.get('email')
            user = User.objects.get(email=email)
            password = request.data.get('password')
            confirm_password = request.data.get('confirm_password')
            serializer = self.serializer_class(data={"password": password,
                                                     "confirm_password":
                                                         confirm_password})
            serializer.is_valid(raise_exception=True)

            if password != confirm_password:
                return Response({"message": "Passwords do not match"},
                                status=status.HTTP_400_BAD_REQUEST)
            user.set_password(password)
            user.save()
        except ExpiredSignatureError:
            message = {"message": "The link has expired"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Password successfully updated"},
                        status=status.HTTP_200_OK)


class SocialAuth(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        provider = request.data['provider']
        strategy = load_strategy(request)
        if 'access_token_secret' in request.data:
            token = {
                'oauth_token': request.data['access_token'],
                'oauth_token_secret': request.data['access_token_secret']
            }
        else:
            token = request.data.get('access_token')
        try:
            backend = load_backend(
                strategy=strategy,
                name=provider,
                redirect_uri=None
            )
        except MissingBackend:
            message = {"error": "Please enter a valid provider."}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = backend.do_auth(token)
        except BaseException:
            return Response({"error": "Invalid token."},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user)
        serializer_data = serializer.data
        serializer_data["token"] = get_jwt_token(user)
        user.is_verified = True
        user.save()
        return Response(serializer_data, status=status.HTTP_200_OK)

