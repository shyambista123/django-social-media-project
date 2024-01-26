from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from auth_app.models import CustomUser
from content_app.models import Post,Comment

from django.contrib import messages

# Create your views here.
@login_required(login_url='/user/login/')
def home(request):
    '''Fetch all posts from database and order them by 
    date posted so that latest post comes first'''
    
    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'dashboard.html', {'posts': posts})

@login_required(login_url='/user/login/')
def post(request):
    '''Get the post data from user and save that post if everything is vaild'''
    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST['caption']
        '''To be a valid post is should contain an image or an valid caption or both'''
        if not image and not caption:
            messages.error(request, "Either image or caption should be provided")
            return redirect('home')

        if caption.isspace():
            messages.error(request, "Caption cannot contain only spaces. Write something...")
            return redirect('home')

        '''Create a post with users provided data and owner as currently logged in user'''
        post = Post.objects.create(image=image, caption=caption, user_id=request.user.id)
        post.save()
        return redirect('home')

    else:
        return render(request,'base.html')

@login_required(login_url='/user/login/')
def edit_post(request, username,post_id):
    '''Get the user by their username'''
    user = get_object_or_404(CustomUser,username=username)
    '''Get posts by post_id and user'''
    post = get_object_or_404(Post, id=post_id, user=user)

    '''Get the data from user and save changes'''
    if request.method == 'POST':
        post.caption = request.POST['caption']
        post.image = request.FILES.get('image', post.image)
        post.save()
        return redirect('home')
    
    return render(request, 'edit-post.html', {'post': post,'user':user})

@login_required(login_url='/user/login/')
def delete_post(request,id):
    '''Get the post by post_id'''
    post = get_object_or_404(Post,id=id)

    '''check if the post owner is current user or not'''
    if request.user == post.user:
        post.delete()
        return redirect('home')

@login_required(login_url='/user/login/')
def like(request, post_id):
    '''Get post by post_id'''
    post = get_object_or_404(Post, id=post_id)

    '''Get currently authenticated user'''
    user = request.user

    '''check if currenly logged in user liked the post or not'''
    if post.likes.filter(id=user.id):
        '''if user already liked the post it remove/unlike post'''
        post.likes.remove(user)
    else:    
        '''if user have not liked the post then like the post'''
        post.likes.add(user)

    '''save post after all these changes'''
    post.save()

    return redirect('post-details',post_id=post.id)

@login_required(login_url='/user/login/')
def user_profile(request,username):
    '''Get the user by username'''
    user = get_object_or_404(CustomUser,username=username)

    '''Get all post of that user'''
    posts = Post.objects.filter(user=user).order_by('-date_posted')

    '''check if the currently logged in user have folloed the user'''
    is_following = request.user.is_following(user)

    '''Count followers'''
    followers_count = user.followers_count()

    '''Counts followings'''
    following_count = user.followings_count()
    
    context = {'users': user, 'username': username, 'posts': posts, 'is_following': is_following,
               'followers_count': followers_count, 'following_count': following_count}

    return render(request,'user-profile.html',context)


@login_required(login_url='/user/login/')
def post_details(request,post_id):
    '''Get the post by post_id'''
    post = get_object_or_404(Post,id=post_id)
    '''Get comments of a particular post by post'''
    comments = Comment.objects.filter(post=post)
    return render(request, 'post-details.html', {'post': post, 'comments': comments})

@login_required(login_url='/user/login/')
def comment(request,post_id):
    '''Get post by post id'''
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        '''prevent that the comment not contains only spaces'''
        text = request.POST.get('comment').strip()
        
        if text:
            Comment.objects.create(user=request.user,post=post,text=text)
            return redirect('post-details', post_id=post.id)  
    
    comments = Comment.objects.filter(post=post)

    return render(request, 'dashboard.html', {'post': post, 'comments': comments})

@login_required(login_url='/user/login/')
def delete_comment(request, comment_id):
    '''Get comment by comment_id'''
    comment = get_object_or_404(Comment, id=comment_id)
    '''allow delete comment only for post owner and comment owner'''
    if comment.user == request.user or comment.post.user == request.user:
        comment.delete()

    return redirect('post-details', post_id=comment.post.id)


@login_required(login_url='/user/login')
def follow(request, username):
    if request.method == 'POST':
        '''Get user by username and follow'''
        user_to_follow = get_object_or_404(CustomUser, username=username)
        request.user.follow(user_to_follow)
    return redirect('user-profile', username=username)

@login_required(login_url='/user/login')
def unfollow(request, username):
    if request.method == 'POST':
        '''Get user by username and unfollow'''
        user_to_unfollow = get_object_or_404(CustomUser, username=username)
        request.user.unfollow(user_to_unfollow)
    return redirect('user-profile', username=username)
