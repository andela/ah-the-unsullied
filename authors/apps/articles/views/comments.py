from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

# local imports
from authors.apps.articles.models import (
    Article, Comments, LikeDislike
)
from authors.apps.articles.renderers import (
    CommentJSONRenderer, LikeArticleJSONRenderer
)
from authors.apps.articles.serializers import (
    CommentSerializer, LikeDislikeSerializer, CommentHistorySerializer
)
from authors.apps.articles.response_messages import error_messages

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
        comment = article.comments.filter(parent=None)
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


class CommentHistoryListView(ListCreateAPIView):
    """Retrieve comments history with comment id."""

    serializer_class = CommentHistorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, slug, comment_id):
        """This is get for comment history"""
        try:
            comment_id = int(comment_id)
        except ValueError:
            message = {'detail': error_messages['non_int']}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        article = Article.objects.filter(slug=slug).first()
        if not article:
            message = {"detail": error_messages['article_404']}
            return Response(message, status.HTTP_404_NOT_FOUND)
        comment = Comments.history.filter(id=comment_id)
        if not comment:
            message = {'detail': error_messages['comment_not_found']}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        if comment.count() == 1:
            message = []
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeDislikeCommentsView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = LikeDislikeSerializer
    renderer_classes = (LikeArticleJSONRenderer,)
    vote_type = None

    def post(self, request, slug, comment_id):
        """""This method posts likes and dislikes to comments"""

        comment = get_object_or_404(Comments, id=comment_id)

        # message to display after like or dislike
        try:
            like_dislike = LikeDislike.objects.get(
                content_type=ContentType.objects.get_for_model(comment),
                author=request.user,
                object_id=comment.id)
            if like_dislike.vote is not self.vote_type:
                like_dislike.vote = self.vote_type
                like_dislike.save(update_fields=['vote'])
            else:
                like_dislike.delete()
        except LikeDislike.DoesNotExist:
            comment.votes.create(author=request.user, vote=self.vote_type)
            comment.save()

        return Response({
            "likes_on_comment": comment.votes.likes().count(),
            "dislikes_on_comment": comment.votes.dislikes().count(),
        },
            content_type="application/json",
            status=status.HTTP_201_CREATED
        )

    def get(self, request, slug, comment_id):

        comment = get_object_or_404(Comments, id=comment_id)

        return Response({
            "likes_on_comment": comment.votes.likes().count(),
            "dislikes_on_comment": comment.votes.dislikes().count(),
        },
            content_type="application/json",
            status=status.HTTP_200_OK
        )
