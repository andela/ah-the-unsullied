"""
Serializer module for the ratings model
"""
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from rest_framework import serializers

from .responses import error_messages
from ..articles.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for the rating model
    """
    rating = serializers.IntegerField(
        required=True,
        validators=[
            MaxValueValidator(5, message=error_messages['maximum_rating']),
            MinValueValidator(1, message=error_messages['minimum_rating'])
        ],
        error_messages={
            'required': 'Please provide a valid rating'
        }
    )
    article = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    def get_average_rating(self, rating_object):
        """Returns an average rating for an article"""
        average_rating = Rating.objects.filter(
            article=rating_object.article.id).aggregate(Avg('rating'))
        return round(average_rating['rating__avg'], 1)

    def get_article(self, rating_object):
        """Returns the slug of the article from the ratings table"""
        return rating_object.article.slug

    class Meta:
        model = Rating
        fields = ('article', 'average_rating', 'rating')
