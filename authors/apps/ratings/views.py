"""
Rating Articles Views module
"""

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Rating
from .serializers import RateSerializers


class RateArticleView(viewsets.ModelViewSet):
    """
    View class for rating articles
    """
    queryset = Rating.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = RateSerializers

    def create(self, request, slug):
        """
        create a rating
        :param: request: rating request
        :param:slug: url field
        :return: 201 response status code with data
        """
        rating = request.data
        user = request.user
        serializer = self.serializer_class(
            data=rating,
            context={'slug': slug, 'user': user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
