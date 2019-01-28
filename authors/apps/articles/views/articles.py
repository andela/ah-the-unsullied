from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, ListCreateAPIView
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.views import status

# local imports
from authors.apps.articles.models import Article
from authors.apps.articles.serializers import (
    ArticleSerializer, UpdateArticleSerializer
)

from authors.apps.articles.renderers import ArticleJSONRenderer
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
