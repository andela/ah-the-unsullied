"""
Serializer module for the ratings model
"""

from django.db.models import Avg
from rest_framework import serializers

from .models import Rating
from ..articles.models import Article
from ..authentication.serializers import UserSerializer
from ..articles.serializers import ArticleSerializer


class RateSerializers(serializers.ModelSerializer):
    """
    Rate Serializer
    :params: serializers.ModelSerializer:
        parent class parameter
    """
    rating = serializers.IntegerField()
    article = ArticleSerializer(read_only=True)
    rating_user = UserSerializer(read_only=True)

    class Meta:
        """
        Meta class
        :adds more setting to the RateSerializer class:
        """
        model = Rating
        fields = ('rating', 'article', 'rating_user')

    def set_average_rating(self, article_object, rating):
        average = rating
        try:
            ratings = Rating.objects.filter(article=article_object.id).all()
            if ratings:
                average = ratings.aggregate(
                    Avg('rating'))['rating__avg']
            article_object.average_rating = average
            article_object.save()
        except Exception as e:
            print(e)

    def create(self, validate_data):

        rate = validate_data['rating']
        slug = self.context.get('slug')
        user = self.context.get('user')

        validate_data['rating_user'] = user
        article = check_article_existence(slug)
        validate_data['article'] = article
        if rate not in range(1, 6):
            raise serializers.ValidationError(
                'Error, rating is between 1 to 5')

        author = article.author
        if author == user:
            raise serializers.ValidationError(
                'Error, you cannot rate your own article'
            )

        rating_instance = None
        try:
            rating_instance = Rating.objects.get(
                rating_user=user,
                article=article
            )
        except:
            "Error, article does not exist"

        if rating_instance:
            """ Update the rating """
            rating_instance.rating = rate
            rating_instance.save()
        else:
            Rating.objects.create(**validate_data)

        self.set_average_rating(article, rate)

        return validate_data


def check_article_existence(slug):
    """
    Checks for the existence of the article and
    returns the article if it exists
    """
    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        raise serializers.ValidationError(
            'Error, Article does not exist'
        )
    return article
