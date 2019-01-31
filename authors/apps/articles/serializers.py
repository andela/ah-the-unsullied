from rest_framework import serializers
from .models import Article, Comments, LikeDislike
from authors.apps.profiles.models import UserProfile
from authors.apps.articles.models import FavoriteArticle
from authors.apps.profiles.serializers import ProfileSerialiazer
from ..utils import get_article_rating


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    body = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    rating = serializers.SerializerMethodField(read_only=True)

    def get_author(self, article):
        author = ProfileSerialiazer(article.author.profiles)
        return author.data

    def get_rating(self, article):
        return get_article_rating(article)

    class Meta:
        model = Article

        fields = ['slug', 'title', 'description', 'body', 'created_at',
                  'updated_at', 'author', 'rating']

    def validate(self, data):

        body = data.get('body', None)
        if body is None:
            raise serializers.ValidationError("body field is required")

        title = data.get('title', None)

        if title is None:
            raise serializers.ValidationError("title field is required")

        description = data.get('description', None)

        if description is None:
            raise serializers.ValidationError("description field is required")

        return {
            'title': title,
            'description': description,
            'body': body,
        }


class UpdateArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    body = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    rating = serializers.SerializerMethodField()

    def get_author(self, article):
        author = ProfileSerialiazer(article.author.profiles)
        return author.data

    def get_rating(self, article):
        return get_article_rating(article)

    class Meta:
        model = Article
        fields = ['slug', 'title', 'description', 'body', 'created_at',
                  'updated_at', 'author', 'rating']


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
                'child': thread.is_Child,
                'body': thread.body,
                'author': ProfileSerialiazer(
                    instance=UserProfile.objects.get(user=thread.author)).data,
                'created_at': self.format_date(thread.created_at),
                'updated_at': self.format_date(thread.updated_at)
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
            'is_Child',
        )


class LikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = '__all__'


class FavouriteSerializer(serializers.ModelSerializer):
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
