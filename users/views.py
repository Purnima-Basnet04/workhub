from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileForm, UserUpdateForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from skills.models import Skill

def register(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        skills_ids = request.POST.get("skills", "")
        skills_ids = [int(i) for i in skills_ids.split(",") if i.isdigit()]
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            if skills_ids:
                profile.skills.set(Skill.objects.filter(id__in=skills_ids))
            messages.success(request, "Registration successful")
            return redirect("/user/login")
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    skills = Skill.objects.filter(is_active=True).values("id", "name")
    return render(request, "pages/users/register.html", {"user_form": user_form, "profile_form": profile_form, "skills": list(skills)})



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
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        skills_str = request.POST.get("skills", "")
        skill_ids = [int(x) for x in skills_str.split(",") if x.isdigit()]
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            profile.skills.set(Skill.objects.filter(id__in=skill_ids))
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileForm(instance=profile)
    skills = Skill.objects.filter(is_active=True).values("id", "name")
    skills_ids_str = ','.join(str(s.id) for s in profile.skills.all())
    skills = Skill.objects.filter(is_active=True).values("id", "name")
    return render(request, "pages/users/profile_update.html", {"user_form": user_form, "profile_form": profile_form, "profile": profile, "skills_ids_str":skills_ids_str, "skills": list(skills)})

def logoutUser(request):
    logout(request)
    messages.success(request, "User Logged out successfully!")
    return redirect('/')