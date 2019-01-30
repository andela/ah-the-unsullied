# local imports
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authors.apps.articles.models import Article, FavoriteArticle
from authors.apps.articles.renderers import ArticleJSONRenderer
from authors.apps.articles.response_messages import (success_messages,
                                                     error_messages)

from authors.apps.articles.serializers import (FavouriteSerializer,
                                               ArticleSerializer)


class CreateArticleView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleSerializer
    renderer_classes = (ArticleJSONRenderer,)
    queryset = Article.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavouriteArticle(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FavouriteSerializer

    def put(self, request, *args, **kwargs):
        article = Article.objects.filter(slug=kwargs['slug']).first()
        if not article:
            msg = {"message": error_messages['article_404']}
            return Response(msg, status.HTTP_404_NOT_FOUND)
        favorite_article = FavoriteArticle.objects.filter(
            user=request.user.id, article=article.id).exists()

        # if article is already a favorite, remove from favorites
        if favorite_article:
            instance = FavoriteArticle.objects.filter(
                user=request.user.id, article=article.id)

            self.perform_destroy(instance)
            msg = {"message": success_messages['remove_favorite']}
            return Response(msg, status.HTTP_200_OK)

        # if article is not a favorite, then make it favorite
        data = {"article": article.id, "user": request.user.id}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        msg = {"message": success_messages['add_favorite']}
        return Response(msg, status.HTTP_200_OK)


class GetFavouriteArticles(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FavouriteSerializer

    def get(self, request):
        fav_article = FavoriteArticle.objects.filter(user=request.user.id)
        serializer = FavouriteSerializer(fav_article, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
