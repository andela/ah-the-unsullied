
from django.db import models
from .utils import get_unique_slug
# local imports
from django.db.models.signals import pre_save
from ..authentication.models import User


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

    class Meta:
        ordering = ['-created_at']


def slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = get_unique_slug(instance, 'title', 'slug')


pre_save.connect(slug_pre_save_receiver, sender=Article)
