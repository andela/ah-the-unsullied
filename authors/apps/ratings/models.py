"""
This module handles rating of articles
"""

from django.db import models

# local imports
from authors.apps.articles.models import Article
from authors.apps.authentication.models import User

# Create your models here.


class Rating(models.Model):
    """
    Rating model
    """
    rating = models.IntegerField(null=False, default=0)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    rating_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __int__(self):
        """
        This special method returns
        ratings data in human readable form
        """
        return self.rating
