
from rest_framework.generics import ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import status

# local imports
from authors.apps.articles.models import Article
from authors.apps.articles.serializers import (ArticleSerializer,
                                               UpdateArticleSerializer)

from authors.apps.articles.renderers import ArticleJSONRenderer


class CreateArticleView(ListCreateAPIView):
    """
        Class handles creating of articles and gets a list of all articles
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleSerializer
    renderer_classes = (ArticleJSONRenderer,)
    queryset = Article.objects.all()

    # Create article with serializer
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        return Response(serializer.data, status.HTTP_201_CREATED)


class GetUpdateDeleteArticle(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    queryset = Article.objects.all()
    serializer_class = UpdateArticleSerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        """
        :param request: user requests to get an article
        :param kwargs: slug field is passed in the url
        :return: data and response if article exists
        """
        try:
            article = Article.objects.get(slug=kwargs['slug'])
        except Article.DoesNotExist:
            message = {"error": "article does not exist"}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(
            instance=article, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """
              :param request: user requests to get an article
              :param kwargs: slug field is passed in the url
              :return: data and response for updated article
              """
        # Get the referenced article
        try:
            article = Article.objects.get(slug=kwargs['slug'])
        except Article.DoesNotExist:
            message = {"error": "article does not exist"}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        # Handle if user is not author
        if request.user.pk != article.author_id:
            message = {"message": "unauthorized to perform this function"}
            return Response(message, status.HTTP_403_FORBIDDEN)

        # save the data
        serializer = self.serializer_class(
            article, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response({
                "message": "article updated successfully",
                "article": serializer.data
            },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Takes slug field from the url, if user handling the request
        is the owner of article they can delete.
        """
        article = Article.objects.filter(slug=kwargs['slug']).first()
        if not article:
            message = {"message": "article not found"}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        # Handle if the user handling request is the author
        if request.user.pk != article.author_id:
            message = {"message": "unauthorized to perform this function"}
            return Response(message, status.HTTP_403_FORBIDDEN)

        # Handle delete after the checks
        article.delete()
        message = {"message": "Article has been deleted"}
        return Response(message, status=status.HTTP_204_NO_CONTENT)
