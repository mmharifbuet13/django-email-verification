from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    # Home page
    path('', home, name="home"),
    # Login page
    path('login/', login_attempt, name="login_attempt"),
    # Registration page
    path('register/', register_attempt, name="register_attempt"),
    # Confirmation of token sent
    path('token/', token_send, name="token_send"),
    # Confirmation of email verificaiton done
    path('success/', success, name="success"),
    # Auth token link in your email
    path('verify/<auth_token>/', verify, name="verify"),
    # Error message link if could not verified
    path('error/', error_page, name="error"),
]