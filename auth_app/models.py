from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    bio = models.CharField(max_length=255,null=True,blank=True)
    is_active = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=255, blank=True, null=True)
    forgot_password_token = models.CharField(max_length=255, blank=True, null=True)
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False)

    def follow(self, user_to_follow):
        if not self.is_following(user_to_follow):
            user_to_follow.followers.add(self)

    def unfollow(self, user_to_unfollow):
        if self.is_following(user_to_unfollow):
            user_to_unfollow.followers.remove(self)

    def is_following(self, user):
        return user.followers.filter(pk=self.pk).exists()

    def get_followers_count(self):
        return self.followers.count()

    def get_following_count(self):
        return self.following.count()

    def save(self, *args, **kwargs):
        if self.is_staff or self.is_superuser:
            self.is_active = True
        super().save(*args, **kwargs)
