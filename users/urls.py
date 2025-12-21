# accounts/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path("register/", register, name="register"),
    path("login", login_user, name="login"),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", profile_update, name="profile-update"),
    path("logout", logoutUser, name="logout"),
]
