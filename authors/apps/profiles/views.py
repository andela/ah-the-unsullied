from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView, ListAPIView)
from rest_framework.response import Response

# Local application imports
from .models import UserProfile
from .serializers import ProfileSerialiazer
from .renderers import ProfileJSONRenderer


class ProfileListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerialiazer
    renderer_classes = (ProfileJSONRenderer,)

    def get_queryset(self):
        queryset = UserProfile.objects.all()
        return queryset


class ProfileDetail(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerialiazer
    renderer_classes = (ProfileJSONRenderer,)

    def get(self, request, username):
        try:
            profile = UserProfile.objects.get(user__username=username)
        except:
            message = {"error": "Profile does not exist."}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            instance=profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username):
        profile = UserProfile.objects.get(user__username=username)
        if profile.user.username != request.user.username:
            # Set image to none to avoid calling cloudinary
            # This will prevent heroku  from interrupting the request
            request.data['image'] = None
            msg = {"error": "You do not have permission to edit this profile."}
            return Response(msg, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        serializer = self.serializer_class(
            instance=request.user.profiles, data=data, partial=True,
            context={
                'request': request}
        )
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowingView(CreateAPIView):
    """
        The class handles the follow and un-follow for users.
        The POST request handles the changing of following
        The Delete request handles un-following a user
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerialiazer
    renderer_classes = (ProfileJSONRenderer,)

    def post(self, request, *args, **kwargs):
        # Get username from the url.
        username = kwargs.get('username')
        # Get the profile related to the username
        if isinstance(check_profile_exists(username), UserProfile):
            profile = check_profile_exists(username)
            # Get the current user who is logged in.
            current_profile = request.user.profiles
            # Ensure user cannot follow themselves
            if current_profile.user.username == profile.user.username:
                message = "you cannot follow yourself"
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            current_profile.toggle_follow(profile.user)
            serializer = self.serializer_class(profile, context={
                'request': request})
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return check_profile_exists(username)


class FollowList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerialiazer
    renderer_classes = (ProfileJSONRenderer,)

    def get(self, request, *args, **kwargs):
        # Get the user to check their following
        username = kwargs.get('username')
        if isinstance(check_profile_exists(username), UserProfile):
            profile = check_profile_exists(username)

        # Get all the list of people following
            queryset = profile.get_all_following()
            serializer = self.serializer_class(queryset, many=True,
                                               context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return check_profile_exists(username)


class FollowerList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerialiazer
    renderer_classes = (ProfileJSONRenderer,)
    queryset = UserProfile.objects.all()

    def get(self, request, *args, **kwargs):
        # Get the user to check their followers
        username = kwargs.get('username')
        if isinstance(check_profile_exists(username), UserProfile):
            profile = check_profile_exists(username)
            queryset = profile.user.followed_by
            serializer = self.serializer_class(queryset, many=True,
                                               context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return check_profile_exists(username)


def check_profile_exists(username):
    try:
        profile = UserProfile.objects.get(user__username=username)
        return profile
    except UserProfile.DoesNotExist:
        message = {"error": "Profile does not exist."}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
