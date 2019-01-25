from authors.apps.articles.models import Rating
from django.db.models import Avg


def get_article_rating(article):
    """
    Returns the average rating of an article
    """

    # searches for the article with the given slug
    # and returns the average ratings
    average_rating = Rating.objects.filter(
        article__slug=article.slug).aggregate(Avg('rating'))
    response = average_rating['rating__avg']

    # set the average rating to 0 if the article has not been rated
    if average_rating['rating__avg'] is None:
        response = average_rating['rating__avg'] = 0
        return response
    return round(response, 1)
