import pdb

from django.db.models import Avg
from rest_framework import serializers

from .models import Article
from authors.apps.profiles.serializers import ProfileSerialiazer
from ..ratings.models import Rating


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
    image = serializers.ImageField(required=False)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['slug', 'title', 'body', 'description',
                  'created_at', 'updated_at', 'author']
        read_only_fields = ('created_at', 'updated_at')

    def get_author(self, article):
        author = ProfileSerialiazer(article.author.profiles)
        return author.data

    def get_average_rating(self, article):
        average = 0
        try:
            ratings = Rating.objects.filter(article=article.id)
            average = round(ratings.all().aggregate(
                Avg('rating'))['rating__avg'], 1)
        except Exception as e:
            print(e)
        return average

    class Meta:
        model = Article
        fields = ['author', 'slug', 'title', 'image', 'description', 'body',
                  'created_at', 'updated_at', 'average_rating']
        read_only_fields = ['slug', 'author', 'created_at', 'updated_at',
                            'username']
