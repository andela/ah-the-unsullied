from django.db import models
from django.db.models.signals import post_save

# Third-party imports
from cloudinary.models import CloudinaryField

# Local imports
from authors.apps.authentication.models import User
from authors.settings import AUTH_USER_MODEL


class UserProfile(models.Model):
        user = models.OneToOneField(AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name='profiles')
        image = CloudinaryField('image', default='')
        bio = models.TextField(null=True, blank=True, max_length=255)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateField(auto_now=True)

        @property
        def username(self):
                return self.user.username

        def __str__(self):
                return str(self.user)


def create_profile_post_receiver(sender, instance, *args, **kwargs):
    if kwargs['created']:
        instance.user_profile = UserProfile.objects.create(user=instance)


post_save.connect(create_profile_post_receiver, sender=User)
