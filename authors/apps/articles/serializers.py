
from rest_framework import serializers

from .models import Article
from authors.apps.profiles.serializers import ProfileSerialiazer


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        author = ProfileSerialiazer(obj.author.profiles)
        return author.data

    class Meta:
        model = Article

        fields = ['slug', 'title', 'description', 'body', 'created_at',
                  'updated_at', 'author']


class RetrieveArticle(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['slug', 'title', 'body', 'description',
                  'created_at', 'updated_at', 'author']

    def get_author(self, obj):
        author = ProfileSerialiazer(obj.author.profiles)
        return author.data


class UpdateArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = ['slug', 'title', 'body', 'description',
                  'created_at', 'updated_at', 'author']
        read_only_fields = ('created_at', 'updated_at')


    def get_author(self, obj):
        author = ProfileSerialiazer(obj.author.profiles)
        return author.data
