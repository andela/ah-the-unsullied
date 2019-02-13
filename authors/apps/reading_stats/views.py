from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .models import ReadingStats
from .serializers import ReadStatsSerializer


class ListReadStatsView(ListAPIView):

    serializer_class = ReadStatsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        current_user = self.request.user
        return ReadingStats.objects.filter(user=current_user)
