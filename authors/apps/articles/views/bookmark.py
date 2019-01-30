# local imports
from rest_framework import status
from rest_framework.generics import (RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authors.apps.articles.models import Article, BookmarkArticleModel
from authors.apps.articles.response_messages import (success_messages,
                                                     error_messages)
from authors.apps.articles.serializers import BookmarkSerializer


class BookmarkArticle(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookmarkSerializer

    def post(self, request, *args, **kwargs):

        filter_article = Article.objects.filter(slug=kwargs['slug']).first()
        if not filter_article:
            msg = {"message": error_messages['article_404']}
            return Response(msg, status.HTTP_404_NOT_FOUND)

        bookmark_article = BookmarkArticleModel.objects.filter(
            user_id=request.user.id, article_id=filter_article.id).exists()

        # # if article is already bookmarked, remove it from bookmarks
        if bookmark_article:
            instance = BookmarkArticleModel.objects.filter(
                user_id=request.user.id, article_id=filter_article.id)
            self.perform_destroy(instance)

            msg = {"message": success_messages['remove_bookmark']}
            return Response(msg, status.HTTP_200_OK)

        # if article is not a bookmarked, then bookmark it
        data = {"article_id": filter_article.id, "user_id": request.user.id}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        msg = {"message": success_messages['add_bookmark']}
        return Response(msg, status.HTTP_200_OK)


class GetBookmarkedArticles(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookmarkSerializer

    def get(self, request):
        fav_article = BookmarkArticleModel.objects.filter(
            user_id=request.user.id)
        serializer = BookmarkSerializer(fav_article, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
