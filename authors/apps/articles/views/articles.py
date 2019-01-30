from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, ListCreateAPIView
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.views import status
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

# local imports
from authors.apps.articles.models import Article, LikeDislike
from authors.apps.articles.serializers import (
    ArticleSerializer, UpdateArticleSerializer, LikeDislikeSerializer
)

from authors.apps.articles.renderers import ArticleJSONRenderer, LikeArticleJSONRenderer
from authors.apps.articles.response_messages import (error_messages,
                                                     success_messages)


class CreateArticleView(ListCreateAPIView):
    """
        Class handles creating of articles
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ArticleSerializer
    renderer_classes = (ArticleJSONRenderer,)
    queryset = Article.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = Article.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        article = request.data.get('article', {})

        if self.request.user.is_verified is False:
            message = error_messages['email_verification']
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)

        context = {"request": request}
        serializer = self.serializer_class(data=article, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetUpdateDeleteArticle(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

    @staticmethod
    def validate_author(request, article):
        if request.user.pk != article.author_id:
            message = error_messages['unauthorised']
            return Response(message, status.HTTP_403_FORBIDDEN)

    def get(self, request, *args, **kwargs):
        """
        :param request: user requests to get an article
        :param kwargs: slug field is passed in the url
        :return: data and response if article exists
        """

        try:
            article = Article.objects.get(slug=kwargs['slug'])
        except Article.DoesNotExist:
            message = error_messages['article_404']
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        serializer = ArticleSerializer(
            instance=article, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """
              :param request: user requests to get an article
              :param kwargs: slug field is passed in the url
              :return: data and response for updated article
              """
        # Get the referenced article

        article_data = request.data.get('article', {})

        try:
            article = Article.objects.get(slug=kwargs['slug'])
        except Article.DoesNotExist:
            message = error_messages['article_404']
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        not_owner = GetUpdateDeleteArticle.validate_author(request, article)
        if not_owner:
            return not_owner

        serializer = UpdateArticleSerializer(
            instance=article, data=article_data, partial=True
        )

        if len(article_data) == 0:
            message = error_messages['null_update']
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Takes slug field from the url, if user handling the request
        is the owner of article they can delete.
        """
        article = Article.objects.filter(slug=kwargs['slug']).first()
        if not article:
            message = error_messages['article_404']
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        not_owner = GetUpdateDeleteArticle.validate_author(request, article)
        if not_owner:
            return not_owner

        # Handle delete after the checks
        article.delete()
        message = success_messages['deleted']
        return Response(message, status=status.HTTP_200_OK)


class LikeDislikeArticleView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = LikeDislikeSerializer
    renderer_classes = (LikeArticleJSONRenderer,)
    vote_type = None

    def post(self, request, slug):
        """""This method posts likes and dislikes"""

        article = get_object_or_404(Article, slug=slug)

        # message to display after like or dislike
        try:
            like_dislike = LikeDislike.objects.get(
                content_type=ContentType.objects.get_for_model(article),
                author=request.user,
                object_id=article.id)
            if like_dislike.vote is not self.vote_type:
                like_dislike.vote = self.vote_type
                like_dislike.save(update_fields=['vote'])
            else:
                like_dislike.delete()
        except LikeDislike.DoesNotExist:
            article.votes.create(author=request.user, vote=self.vote_type)
            article.save()

        return Response({
            "likes": article.votes.likes().count(),
            "dislikes": article.votes.dislikes().count(),
                },
                content_type="application/json",
                status=status.HTTP_201_CREATED
            )

    def get(self, request, slug):

        article = get_object_or_404(Article, slug=slug)

        return Response({
            "likes": article.votes.likes().count(),
            "dislikes": article.votes.dislikes().count(),
                },
                content_type="application/json",
                status=status.HTTP_200_OK
            )
