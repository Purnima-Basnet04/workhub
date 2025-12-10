from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def register(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = user.profile
            for field in profile_form.cleaned_data:
                setattr(profile, field, profile_form.cleaned_data[field])
            profile.save()
            messages.success(request, "Registration successful")
            return redirect("/user/login")
        else:
            print(user_form.errors)
            print(profile_form.errors)
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    return render(request, "pages/users/register.html", {"user_form": user_form, "profile_form": profile_form, })


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    errors = {}
    username = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        check_user = User.objects.filter(username=username).exists() 
        if check_user:
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user:
                login(request, authenticated_user) 
                messages.success(request, "You have successfully logged in")
                return redirect('/dashboard')
            else:
                messages.error(request, "Invalid Password!")
                errors['password'] = "Invalid Password!" 
        else:
            messages.error(request, "User doesnot exist")
            errors['username'] = "User doesnot exist."       
        if errors:
            return render(request, 'pages/users/login.html', {'errors': errors}) 
    return render(request, 'pages/users/login.html', {'errors': errors, 'username': username})


@login_required(login_url='/users/login')
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, "pages/users/profile.html", {"profile": profile})

@login_required(login_url='/users/login')
def profile_update(request):
    user = request.user
    profile = user.profile
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        user_form = UserRegistrationForm(instance=user)
        profile_form = ProfileForm(instance=profile)
    return render(request, "pages/users/profile_update.html", {"user_form": user_form, "profile_form": profile_form})

def logoutUser(request):
    logout(request)
    messages.success(request, "User Logged out successfully!")
    return redirect('/')