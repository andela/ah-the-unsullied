from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Local application imports
from .models import UserProfile
from .serializers import ProfileSerialiazer
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer


class ProfileListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerialiazer
    renderer_classes = (ProfilesJSONRenderer,)

    def get_queryset(self):
        queryset = UserProfile.objects.all().exclude(user=self.request.user)
        return queryset


class ProfileDetail(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerialiazer
    renderer_classes = (ProfileJSONRenderer,)

    def get(self, request, username):
        try:
            profile = UserProfile.objects.get(user__username=username)
        except:
            message = { "error": "Profile does not exist."}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(profile)
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
            instance=request.user.profiles, data=data, partial=True
        )
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
