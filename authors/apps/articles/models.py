from django.db import models
from cloudinary.models import CloudinaryField
from .utils import get_unique_slug
# local imports
from ..authentication.models import User


# Create your models here.

class Article(models.Model):
    slug = models.SlugField(unique=True, max_length=253, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author')
    title = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=230, blank=False)
    body = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'title', 'slug')
            super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
