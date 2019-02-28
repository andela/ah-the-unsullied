from django.contrib.contenttypes.fields import GenericRelation, \
    GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save
from simple_history.models import HistoricalRecords

# Third party imports
from taggit.managers import TaggableManager

# local imports
from ..authentication.models import User
from .utils import get_unique_slug

"""
    Articles
"""


class LikeDislikeManager(models.Manager):
    """This is model manager for likes and dislikes data"""

    def likes(self):
        """
        get all the likes for an object
        """
        return self.get_queryset().filter(vote=True)

    def dislikes(self):
        """
        get all the dislikes for an object
        """
        return self.get_queryset().filter(vote=False)


class LikeDislike(models.Model):
    """This class defines data for the likes and dislikes."""

    LIKE = True
    DISLIKE = False

    VOTES = (
        (DISLIKE, 'Dislike'),
        (LIKE, 'Like')
    )

    vote = models.BooleanField(verbose_name='vote', choices=VOTES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()


# Create your models here.
class Article(models.Model):
    slug = models.SlugField(max_length=253, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author')
    title = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=230, blank=False)
    body = models.TextField(blank=False)
    tag_list = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = GenericRelation(LikeDislike, related_query_name='articles')
    read_time = models.TextField(default='null')
    is_reported = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.title)


class Comments(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField(max_length=200)
    author = models.ForeignKey(User, related_name='author_rel',
                               on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='comments',
                                on_delete=models.CASCADE, null=False)
    parent = models.ForeignKey('self', null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name='threads')
    history = HistoricalRecords()
    votes = GenericRelation(LikeDislike, related_query_name='comments')

    def __str__(self):
        return str(self.body)


def slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = get_unique_slug(instance, 'title', 'slug')


pre_save.connect(slug_pre_save_receiver, sender=Article)


class FavoriteArticle(models.Model):
    """Favorite Article model"""

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.article)


class Rating(models.Model):
    """
    Rating model
    """
    rating = models.FloatField(null=False, default=0)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



class BookmarkArticleModel(models.Model):
    """Bookmark Article model"""
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.article)


class ReportArticle(models.Model):
    """Report Article model"""

    slug = models.CharField(max_length=253, blank=True)
    reporter_id = models.CharField(max_length=253, blank=True)
    author_id = models.CharField(max_length=253, blank=True)
    message = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.slug)

class HighlightArticleModel(models.Model):
    body = models.TextField()
    author = models.ForeignKey(User, related_name='author_relate',
                               on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='highlight',
                                on_delete=models.CASCADE)
    highlited_article = models.TextField(blank=True, null=True)
    begin_index = models.IntegerField(blank=True, null=True)
    end_index = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.body)

    class Meta:
        ordering = ['-created_at']
