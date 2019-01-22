from rest_framework import serializers

from .models import Article
from authors.apps.profiles.serializers import ProfileSerialiazer


class ArticleSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()
    body = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)

    def get_author(self, article):
        author = ProfileSerialiazer(article.author.profiles)
        return author.data

    class Meta:
        model = Article

        fields = ['slug', 'title', 'description', 'body', 'created_at',
                  'updated_at', 'author']

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

    def get_author(self, article):
        author = ProfileSerialiazer(article.author.profiles)
        return author.data

    class Meta:
        model = Article
        fields = ['slug', 'title', 'description', 'body', 'created_at',
                  'updated_at', 'author']
