from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('post/',views.post,name='post'),
    path('edit-post/<str:username>/<int:post_id>/',views.edit_post,name='edit-post'),
    path('delete-post/<int:id>/',views.delete_post,name='delete-post'),
    path('<int:post_id>/like/', views.like, name='like'),
    path('user-profile/<str:username>/',views.user_profile,name='user-profile'),
    path('post-details/<int:post_id>/',views.post_details,name='post-details'),
    path('add-comment/<int:post_id>/',views.comment,name='comment'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete-comment'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
]
