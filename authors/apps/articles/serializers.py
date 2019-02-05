import readtime
from rest_framework import serializers
from .models import Article, Comments, LikeDislike, ReportArticle
from authors.apps.profiles.models import UserProfile
from taggit_serializer.serializers import (
    TagListSerializerField,
    TaggitSerializer
)
from authors.apps.articles.models import FavoriteArticle, BookmarkArticleModel
from authors.apps.profiles.serializers import ProfileSerialiazer
from ..utils import get_article_rating
from taggit.models import Tag


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    body = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    rating = serializers.SerializerMethodField(read_only=True)
    tag_list = TagListSerializerField()
    read_time = serializers.SerializerMethodField()

    def get_author(self, article):
        author = ProfileSerialiazer(article.author.profiles)
        return author.data

    def get_rating(self, article):
        return get_article_rating(article)

    def get_read_time(self, article):
        read_time = readtime.of_text(article.body)
        return str(read_time)

    class Meta:
        model = Article
        fields = ['slug', 'title', 'description', 'body', 'tag_list',
                  'created_at', 'updated_at', 'author', 'rating', 'read_time']


class UpdateArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    body = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    rating = serializers.SerializerMethodField()
    tag_list = TagListSerializerField()
    read_time = serializers.SerializerMethodField()

    def get_author(self, article):
        author = ProfileSerialiazer(article.author.profiles)
        return author.data

    def get_rating(self, article):
        return get_article_rating(article)

    def get_read_time(self, article):
        read_time = readtime.of_text(article.body)
        return str(read_time)

    class Meta:
        model = Article
        fields = ['slug', 'title', 'description', 'body', 'tag_list',
                  'created_at', 'updated_at', 'author', 'rating', 'read_time']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    article = serializers.SerializerMethodField()
    body = serializers.CharField(
        max_length=200,
        required=True,
        error_messages={
            'required': 'Comments field cannot be blank'
        }
    )

    def get_author(self, comment):
        author = ProfileSerialiazer(comment.author.profiles)
        return author.data

    def get_article(self, comment):
        article = ArticleSerializer(comment.article)
        return article.data

    def format_date(self, date):
        return date.strftime('%d %b %Y %H:%M:%S')

    def to_representation(self, instance):
        """
        override representation for custom output
        """
        threads = [
            {
                'id': thread.id,
                'body': thread.body,
                'author': ProfileSerialiazer(
                    instance=UserProfile.objects.get(user=thread.author)).data,
                'created_at': self.format_date(thread.created_at),
                'updated_at': self.format_date(thread.updated_at),
            } for thread in instance.threads.all()
        ]

        thread_comment = super(
            CommentSerializer, self).to_representation(instance)
        thread_comment['created_at'] = self.format_date(instance.created_at)
        thread_comment['updated_at'] = self.format_date(instance.updated_at)
        thread_comment['article'] = instance.article.title
        thread_comment['threads'] = threads
        del thread_comment['parent']

        return thread_comment

    class Meta:
        model = Comments
        fields = (
            'id',
            'body',
            'created_at',
            'updated_at',
            'author',
            'article',
            'parent',
            'parent_id'
        )


class LikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = '__all__'


class FavouriteSerializer(serializers.ModelSerializer):
    """This serializer is used to favourite an article"""
    author = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()

    def get_author(self, favorite):
        author = favorite.article.author.username
        return author

    def get_title(self, favorite):
        title = favorite.article.title
        return title

    def get_slug(self, favorite):
        slug = favorite.article.slug
        return slug

    class Meta:
        model = FavoriteArticle

        fields = ('title', 'slug', 'author', 'article', 'user')


class CustomTagSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Tag
        fields = ('name',)


class BookmarkSerializer(serializers.ModelSerializer):
    """This serializer is used for  bookmarking article"""
    author_name = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()

    def get_author_name(self, bookmark):
        author = bookmark.article_id.author.username
        return author

    def get_title(self, bookmark):
        title = bookmark.article_id.title
        return title

    def get_slug(self, bookmark):
        slug = bookmark.article_id.slug
        return slug

    class Meta:
        model = BookmarkArticleModel
        fields = ('title', 'slug', 'author_name', 'user_id', 'article_id')


class CommentHistorySerializer(serializers.ModelSerializer):
    """
    This class handles the history of the comment edited
    """

    class Meta:
        model = Comments
        fields = ('id', 'body', 'created_at', 'updated_at')


class ReportArticleSerializer(serializers.ModelSerializer):
    message = serializers.CharField(required=True)

    class Meta:
        model = ReportArticle
        fields = ('slug', 'author_id', 'message', 'reporter_id')
