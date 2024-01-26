import uuid
from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings as seeting

from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def register(request):
    ''' This view handles user registration by processing the POST request with user data. It validates the if 
    username and password are valid(not only spaces) and uniqueness of the username and email, creates a new user if they are unique, 
    generates a verification code, sends a verification email, and redirects the user accordingly. 
    In case of a GET request, renders the registration form.
    '''
    if request.method == 'POST':
        f_name = request.POST['first_name']
        l_name = request.POST['last_name']
        username = request.POST['username'].strip()
        email = request.POST['email']
        password = request.POST['password'].strip()
        profile_image = request.FILES.get('profile_image')
        bio = request.POST['bio']

        if not username or not password:
            messages.error(request, "Username and password cannot be empty or contain only spaces")
            return redirect('register')

        else:
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request,"User with this username already exists")
                return redirect('register')
            elif CustomUser.objects.filter(email=email).exists():
                    messages.info(request,"User with this email already exists")
                    return redirect('register')
            else:
                user = CustomUser.objects.create_user(
                    username=username,
                    first_name=f_name,
                    last_name=l_name,
                    email=email,
                    password=password,
                    profile_image=profile_image,
                    bio=bio,
                )

                verification_code = str(uuid.uuid4())

                user.verification_code = verification_code
                user.save()

                '''Let's suppose Django app is running on 'http://localhost:8000/' and the result of the reverse function is '/verify-email/actual_verification_code_generated/',
                then request.build_absolute_uri('/verify-email/abc123/') would give 'http://localhost:8000/verify-email/abc123/'''

                verification_url = request.build_absolute_uri(reverse('verify_email', args=[verification_code]))

                subject = 'Verify your email'
                message_plain = f'Click the following link to verify your email: {verification_url}'
                message_html = f'Click the following link to verify your email: <a href="{verification_url}" target="_blank">{verification_url}</a>'

                from_email = seeting.DEFAULT_FROM_EMAIL
                to_email = user.email

                send_mail(subject, message_plain, from_email, [to_email], html_message=message_html)

                # print(message_plain+message_html)

                messages.success(request, "User registered successfully. Now click the link in your email and verify the email to login.")
                return redirect('login')
    else:
        return render(request,'register.html')
    

def verify_email(request, verification_code):
    try:
        '''Attempt to retrieve a user with the provided verification code'''
        user = CustomUser.objects.get(verification_code=verification_code, is_active=False)

        '''Make user account active and clear the verification code and save user'''
        user.is_active = True 
        user.verification_code = None
        user.save()
        messages.success(request, 'Your email has been verified. You can now log in.')
    except CustomUser.DoesNotExist:
        messages.error(request, 'Invalid verification code.')

    return redirect('login')


def login(request):
    if request.method == 'POST':
        '''take input username and password from user'''
        username = request.POST['username']
        password = request.POST['password']

        '''Authenticate the user using the user inputs username and password'''
        user = auth.authenticate(username = username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("home")
        else:
            messages.error(request,"Invalid Credential!!!")
            return redirect('login')
    else:
        return render(request,'login.html')

@login_required(login_url='/user/login/')
def logout(request):
    '''Logout the logged in user'''
    auth.logout(request)
    messages.success(request,"You are logged out successfully !!!")
    return redirect('login')

@login_required(login_url='/user/login/')
def edit_profile(request):
    '''Get the currently authenticated user'''
    user = request.user

    '''Update the user based on the data provided by user'''
    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.username = request.POST['username']
        user.bio = request.POST['bio']
        user.profile_image = request.FILES.get('profile_image', user.profile_image)
        user.save()
        return redirect('user-profile', username=user.username)

    return render(request,'edit-profile.html',{'user':user})


@login_required(login_url='/user/login/')
def settings(request):
    return render(request,'settings.html')

@login_required(login_url='/user/login/')
def change_password(request):
    '''Get the currently authenticated user'''
    user = request.user

    '''Get data from user and check and update'''
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        if user.check_password(old_password):
            if new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                '''Re-authenticate the user to update the session'''
                authenticated_user = auth.authenticate(username=user.username, password=new_password1)
                auth.login(request, authenticated_user)
                messages.success(request, 'Password changed successfully!')
                return redirect('change-password')
            else:
                messages.error(request, 'New passwords do not match.')
        else:
            messages.error(request, 'Incorrect old password.')

    return render(request,'settings.html',{'user':user})

@login_required(login_url='/user/login/')
def delete_account(request):
    '''Get the currently authenticated user'''
    user = request.user
    '''ask password and check password and process'''
    if request.method == 'POST':
        password = request.POST['password']
        
        '''check the user's input password with user's actual password'''
        if user.check_password(password):
            user.delete()
            messages.success(request,"Account deleted successfully")
            return redirect('login')
        else:
            messages.error(request,"Wrong Password, Please enter correct password to delete your account!!!")
            return redirect('settings')
    else:
        return render(request,'settings.html',{'user':user})


def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
        '''Get the email input and find user with that email
        if find process the password reset by sending email
        if user is not find, show an error message '''
        try:
            user = CustomUser.objects.get(email=email)
            forgot_password_token = str(uuid.uuid4())

            user.forgot_password_token = forgot_password_token
            user.save()

            '''Constructs the absolute URL for the 'reset-password' link using the current request's domain
            and the 'reset-password' URL pattern. Includes the forgot_password_token as part of the URL.'''

            forgot_password_url = request.build_absolute_uri(reverse('reset-password', args=[forgot_password_token]))

            subject = 'Reset your password'
            message_plain = f'Click the following link to reset your password: {forgot_password_url}'
            message_html = f'Click the following link to reset your password: <a href="{forgot_password_url}" target="_blank">{forgot_password_url}</a>'

            from_email = seeting.DEFAULT_FROM_EMAIL
            to_email = user.email
            
            send_mail(subject, message_plain, from_email, [to_email], html_message=message_html)
            messages.success(request, "We have sent you a password reset link. Follow that link to reset the password")
            return redirect('forgot-password')

        except CustomUser.DoesNotExist:
            messages.error(request, 'User not found with this email')

    return render(request, 'forgot-password.html')

def reset_password(request, forgot_password_token):
    try:
        '''Attempt to retrive user with forgot_password_token'''
        user = CustomUser.objects.get(forgot_password_token=forgot_password_token)
        
        '''if token is vaild and user is find process other reseting password'''
        if request.method == 'POST':
            '''Get new password from user and set that password to that user and clear the forgot_password_token'''
            new_password = request.POST.get('new_password')

            if new_password:
                user.set_password(new_password)
                user.forgot_password_token = None
                user.save()
                messages.success(request, 'Password reset successfully. You can now log in with your new password.')
                return redirect('login')
            else:
                messages.error(request, 'Please provide a new password.')

        return render(request, 'reset-password.html', {'forgot_password_token': forgot_password_token})
    
    except CustomUser.DoesNotExist:
        '''Throw error if user is not found with provided email'''
        messages.error(request, 'Invalid password reset link')
        return redirect('forgot-password')
