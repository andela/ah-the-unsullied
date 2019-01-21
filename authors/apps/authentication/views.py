from rest_framework import status
from rest_framework.generics import (RetrieveUpdateAPIView, CreateAPIView,
                                     ListAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.response import Response
from django.template.loader import render_to_string

from django.urls import reverse
from django.core.mail import send_mail

# Local imports
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
    ActivateSerializer
)
from .models import User
from .activate import account_activation_token


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
            host=request.get_host(),
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
