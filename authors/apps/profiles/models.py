
from django.db import models
from django.db.models.signals import post_save

# Local imports
from authors.apps.authentication.models import User
from authors.settings import AUTH_USER_MODEL


class UserProfileManager(models.Manager):

    def all(self):
        queryset = self.get_queryset().all()
        try:
            if self.instance:
                queryset = queryset.exclude(user=self.instance)
        except:
            pass
        return queryset


class UserProfile(models.Model):
        user = models.OneToOneField(AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name='profiles')
        image = models.URLField(blank=True,null=True)
        bio = models.TextField(null=True, blank=True, max_length=255)
        following = models.ManyToManyField(AUTH_USER_MODEL, blank=True,
                                           related_name='followed_by')
        followed_at = models.DateField(auto_now_add=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateField(auto_now=True)

        objects = UserProfileManager()

        @property
        def username(self):
                return self.user.username

        def __str__(self):
                return str(self.user.username)

        def get_all_following(self):
            # Get all following list
            users = self.following.all()
            profile_list = []
            for item in users:
                profile_list.append(item.profiles)
            return profile_list

        def follow(self, profile):
            # Add profile to following list
            return self.following.add(profile)

        def unfollow(self, profile):
            # Remove profile to following list
            return self.following.remove(profile)

        def toggle_follow(self, profile):
            # Toggles follow and un-follow
            if self.check_if_following(profile):
                return self.unfollow(profile)
            return self.follow(profile)

        def check_if_following(self, profile):
            # Check if following
            return self.following.filter(pk=profile.pk).exists()


def create_profile_post_receiver(sender, instance, *args, **kwargs):
    if kwargs['created']:
        instance.user_profile = UserProfile.objects.create(user=instance)


post_save.connect(create_profile_post_receiver, sender=User)
