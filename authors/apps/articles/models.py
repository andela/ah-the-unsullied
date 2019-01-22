from django.db import models
from .utils import get_unique_slug
from django.db.models.signals import pre_save
from django.db import models
from cloudinary.models import CloudinaryField
from .utils import get_unique_slug

# local imports
from ..authentication.models import User

"""
    Articles
"""


# Create your models here.
class Article(models.Model):
    slug = models.SlugField(max_length=253, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author')
    title = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=230, blank=False)
    body = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.title)


class Comments(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    body = models.TextField(max_length=200)
    is_Child = models.BooleanField(default=False)
    author = models.ForeignKey(User, related_name='author_rel',
                               on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='comments',
                                on_delete=models.CASCADE, null=False)
    parent = models.ForeignKey('self', null=True, blank=True,
                               on_delete=models.CASCADE, related_name='threads')

    def __str__(self):
        return str(self.body)

    class Meta:
        ordering = ['-created_at']


def slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = get_unique_slug(instance, 'title', 'slug')
