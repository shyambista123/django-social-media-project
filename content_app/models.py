from django.db import models
from auth_app.models import CustomUser

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')
    caption = models.TextField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser,related_name='post_likes',blank=True)
    comments = models.ManyToManyField(CustomUser, through='Comment', related_name='commented_posts')

    def __str__(self):
        return self.caption
    
    def no_of_likes(self):
        return self.likes.count()
    
    def no_of_comments(self):
        return self.comments.count()


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text