from django.db import models

# Create your models here.
from authors.settings import AUTH_USER_MODEL
from authors.apps.articles.models import Article


class ReadingStats(models.Model):

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.article.title
