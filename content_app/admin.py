from django.contrib import admin

from content_app.models import Post,Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
