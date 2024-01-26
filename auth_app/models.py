from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    bio = models.CharField(max_length=255,null=True,blank=True)
    is_active = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=255, blank=True, null=True)
    forgot_password_token = models.CharField(max_length=255, blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    def follow(self, user):
        """
        Follow the given user.
        """
        if not self.is_following(user):
            self.followers.add(user)

    def unfollow(self, user):
        """
        Unfollow the given user.
        """
        if self.is_following(user):
            self.followers.remove(user)

    def is_following(self, user):
        """
        Check if the user is already following the given user.
        """
        return self.followers.filter(pk=user.pk).exists()

    def followers_count(self):
        """
        Count the number of followers.
        """
        return self.following.count()

    def followings_count(self):
        """
        Count the number of users being followed.
        """
        return self.followers.count()



    def save(self, *args, **kwargs):
        if self.is_staff or self.is_superuser:
            self.is_active = True
        super().save(*args, **kwargs)
