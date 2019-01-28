from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView,
    CreateAPIView
)
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework import status

# local imports
from authors.apps.articles.models import (
    Article, Comments
)
from authors.apps.articles.serializers import (
    ArticleSerializer, CommentSerializer
)
from authors.apps.articles.renderers import (
    ArticleJSONRenderer, CommentJSONRenderer
)
from authors.apps.articles.views import articles

# Create your views here.
class CommentsListView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comments.objects.all()
    renderer_classes = (CommentJSONRenderer,)

    def create(self, request, slug, *args, **kwargs):
        serializer_context = {
            'request': request,
            'article': get_object_or_404(Article, slug=self.kwargs["slug"])
        }

        article = Article.objects.filter(slug=slug).first()
        data = request.data
        serializer = self.serializer_class(
            data=data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, article_id=article.pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, slug, *args, **kwargs):

        article = Article.objects.filter(slug=slug).first()
        if not article:
            message = {"error": "Article doesn't exist"}
            return Response(message, status.HTTP_404_NOT_FOUND)
        comment = article.comments.filter(is_Child=False)
        serializer = self.serializer_class(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentsRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView,
                                    CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comments.objects.all()
    renderer_classes = (CommentJSONRenderer,)
    lookup_field = 'id'

    def create(self, request, slug, id):
        """Method for creating a child comment on parent comment."""

        context = super(CommentsRetrieveUpdateDestroy,
                        self).get_serializer_context()

        article = Article.objects.filter(slug=slug).first()
        if isinstance(article, dict):
            return Response(article, status=status.HTTP_404_NOT_FOUND)
        parent = article.comments.filter(id=id).first().pk
        if not parent:
            message = {'error': 'Comment not found.'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        # How I want to post child comment
        body = request.data.get('comment', {}).get('body', {})

        data = {
            'body': body,
            'parent': parent,
            'article': article.pk,
            'is_Child':True
        }

        serializer = self.serializer_class(
            data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, article_id=article.pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, slug, id):
        try:
            article = Article.objects.filter(slug=slug).first()
        except:
            message = {"error": "Article doesn't exist"}
            return Response(message, status.HTTP_404_NOT_FOUND)
        try:
            comment = article.comments.filter(id=id).first().pk
            return super().get(request, comment)
        except:
            message = {"error": "comment doesn't exist"}
            return Response(message, status.HTTP_404_NOT_FOUND)

    def update(self, request, slug, id):

        article = Article.objects.filter(slug=slug).first()
        if not article:
            message = {"error": "Article doesn't exist"}
            return Response(message, status.HTTP_404_NOT_FOUND)
        comment = article.comments.filter(id=id).first()
        if not comment:
            message = {"message": "Comment does not exist"}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        update_comment = request.data.get('comment', {})['body']
        data = {
            'body': update_comment,
            'article': article.pk,
        }
        serializer = self.serializer_class(comment, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, slug, id):
        article = Article.objects.filter(slug=slug).first()
        if not article:
            message = {"error": "Article doesn't exist"}
            return Response(message, status.HTTP_404_NOT_FOUND)
        try:
            comment = article.comments.filter(id=id).first().pk
        except:
            message = {"error": "comment doesn't exist"}
            return Response(message, status.HTTP_404_NOT_FOUND)
        super().delete(self, request, comment)
        message = {"message": "Comment deleted successfully"}
        return Response(
            message, status.HTTP_200_OK)
