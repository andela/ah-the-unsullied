from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import (
    GenericAPIView
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response

from .responses import (
    error_messages, successful_submission, success_messages
)
from .serializers import RatingSerializer
from ..articles.models import Article, Rating
from ..utils import get_article_rating


class ArticleRatingAPIView(GenericAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @staticmethod
    def get_article(slug):
        """Returns the first record in the articles table with the slug"""
        article = Article.objects.all().filter(slug=slug).first()
        return article

    def post(self, request, slug):
        """POST Request to rate an article"""
        rating = request.data
        article = self.get_article(slug)

        if check_article_exists(article):
            return check_article_exists(article)

        if request.user.id == article.author.id:
            return Response(
                error_messages['unauthorized'],
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            current_article_rating = Rating.objects.get(
                user=request.user.id,
                article=article.id
            )
            serializer = self.serializer_class(
                current_article_rating, data=rating)
        except Rating.DoesNotExist:
            serializer = self.serializer_class(data=rating)

        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, article=article)
        return Response({
            'message': successful_submission['message'],
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def get(self, request, slug):
        """Returns an article's ratings"""
        article = self.get_article(slug)
        rating = None

        # check if the article exists
        if check_article_exists(article):
            return check_article_exists(article)

        # if the user is authenticated fetch their ratings
        if request.user.is_authenticated:
            try:
                rating = Rating.objects.get(
                    user=request.user, article=article
                )
            except Rating.DoesNotExist:
                raise NotFound(
                    detail=error_messages['not_rated']
                )
        # for unauthenticated users
        if rating is None:
            average_rating = get_article_rating(article)

            if request.user.is_authenticated is False:
                return Response({
                    'article': article.slug,
                    'average_rating': average_rating,
                    'rating': error_messages['login']
                }, status=status.HTTP_200_OK)
        serializer = self.serializer_class(rating)
        return Response({
            'message': success_messages['message'],
            'data': serializer.data
        }, status=status.HTTP_200_OK)


def check_article_exists(article):
    if not article:
        return Response(
            error_messages['not_exist'],
            status=status.HTTP_404_NOT_FOUND
        )
