import uuid

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login

from .models import *

def home(request):
    return render(request, 'Home/home.html')

def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('login_username')
        password = request.POST.get('login_password')

        user_obj = User.objects.filter(username=username).first()

        if user_obj is None:
            messages.success(request, "User does not exist")
            return redirect('login_attempt')
        
        profile_obj =  Profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request, "Please verify your email first")      
            return redirect('login_attempt')
        
        user = authenticate(username=username, password=password)
        if user is None:
            return redirect('login_attempt')

        login(request, user)
        return redirect('home')

    return render(request, 'accounts/login.html')

def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:

            if User.objects.filter(username=username).first():
                messages.success(request, "Username already registered")
                return redirect('login_attempt')
            
            if User.objects.filter(email=email).first():
                messages.success(request, "Email already registered")
                return redirect('login_attempt')
            
            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()

            auth_token = str(uuid.uuid4())
            

            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registrations(email, auth_token)

            return redirect('token_send')

        except Exception as error:
            print(error)

    return render(request, 'accounts/register.html')

def success(request):
    return render(request, 'accounts/success.html')

def token_send(request):
    return render(request, 'accounts/token_send.html')

def verify(request, auth_token):

    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            return redirect('success')
        else:
            return redirect('error')
    except Exception as error:
        print(error)

def error_page(request):
    return render(request, 'accounts/error.html')


# ! This is the helper method
def send_mail_after_registrations(email, token):
    subject = "Your account needs to be verified"
    message =  f'Hi! Click on the link to verify your account http://127.0.0.1:8000/verify/{token}'
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    send_mail(subject, message, from_email, to_email)