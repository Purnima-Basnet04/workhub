from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from skills.models import Skill
from .models import Profile, Experience, Education, Certification, SocialLink, Project
from .forms import *
from .utils import calculate_total_experience


def register(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")

    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            messages.success( request, "Registration successful. Please login to complete your profile." )
            return redirect("/user/login")
    else:
        user_form = UserRegistrationForm()
    return render(request, "pages/users/register.html", {"user_form": user_form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")
    errors = {}
    username = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        check_user = User.objects.filter(username=username).exists()

        if check_user:
            authenticated_user = authenticate(
                request, username=username, password=password
            )
            if authenticated_user:
                login(request, authenticated_user)
                messages.success(request, "You have successfully logged in")
                return redirect("/dashboard")
            else:
                messages.error(request, "Invalid Password!")
                errors["password"] = "Invalid Password!"
        else:
            messages.error(request, "User does not exist")
            errors["username"] = "User does not exist."
        if errors:
            return render(request, "pages/users/login.html", {"errors": errors})

    return render(
        request, "pages/users/login.html", {"errors": errors, "username": username}
    )


def logoutUser(request):
    logout(request)
    messages.success(request, "User logged out successfully!")
    return redirect("/")


@login_required(login_url="/user/login")
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    skills = Skill.objects.filter(is_active=True).values("id", "name")
    skills_ids_str = ",".join(str(s.id) for s in profile.skills.all())
    experience_duration = calculate_total_experience(profile.experiences.all())
    return render(  request, "pages/users/profile.html", { "profile": profile, "experience_duration": experience_duration, "skills_ids_str": skills_ids_str, "skills": list(skills)})


@login_required(login_url="/user/login")
def profile_update(request):
    user = request.user
    profile = user.profile

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if profile_form.is_valid() and user_form.is_valid():
            profile = profile_form.save(commit=False)
            user = user_form.save(commit=False)
            user.save()
            profile.user = user
            profile.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
        else:
            return render( request,"pages/users/profile_update.html", {"profile_form": profile_form, "user_form": user_form,"profile": profile})
    else:
        profile_form = ProfileForm(instance=profile)
        user_form = UserUpdateForm(instance=user)
        return render( request, "pages/users/profile_update.html", { "profile_form": profile_form, "user_form": user_form, "profile": profile })


@login_required(login_url="/user/login")
def add_skill(request):
    profile = request.user.profile
    if request.method == "POST":
        skills_str = request.POST.get("skills", "")
        skill_ids = [int(x) for x in skills_str.split(",") if x.isdigit()]
        profile.skills.set(Skill.objects.filter(id__in=skill_ids))
        messages.success(request, "Skills updated successfully.")
        return redirect("profile")
    else:
        return redirect("profile")

@login_required(login_url="/user/login")
def add_or_edit_experience(request, id=None):
    profile = request.user.profile
    experience = None

    if id:
        experience = get_object_or_404(Experience, id=id, profile=profile)

    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.profile = profile
            exp.save()
            messages.success( request,  ("Experience updated successfully." if id else "Experience added successfully."  ))
            return redirect("profile")
    else:
        form = ExperienceForm(instance=experience)

    return render(  request, "pages/users/profile_form.html", {
            "form": form,
            "page_title": "Edit Experience" if id else "Add Experience",
            "page_subtitle": ( "Update your work experience details." if id else "Add your work experience details." )
            })

@login_required(login_url="/user/login")
def add_or_edit_education(request, id=None):
    profile = request.user.profile
    education = None

    if id:
        education = get_object_or_404(Education, id=id, profile=profile)

    if request.method == "POST":
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            edu = form.save(commit=False)
            edu.profile = profile
            edu.save()
            messages.success( request, ( "Education updated successfully."  if id else "Education added successfully." ) )
            return redirect("profile")
    else:
        form = EducationForm(instance=education)

    return render( request, "pages/users/profile_form.html", {
            "form": form,
            "page_title": "Edit Education" if id else "Add Education",
            "page_subtitle": ( "Update your educational qualifications." if id else "Add your educational qualifications.")
            })


@login_required(login_url="/user/login")
def add_or_edit_certification(request, id=None):
    profile = request.user.profile
    certification = None

    if id:
        certification = get_object_or_404(Certification, id=id, profile=profile)

    if request.method == "POST":
        form = CertificationForm(request.POST, instance=certification)
        if form.is_valid():
            cert = form.save(commit=False)
            cert.profile = profile
            cert.save()
            messages.success(request, ("Certification updated successfully." if id else "Certification added successfully." ))
            return redirect("profile")
    else:
        form = CertificationForm(instance=certification)

    return render( request, "pages/users/profile_form.html", {
            "form": form,
            "page_title": "Edit Certification" if id else "Add Certification",
            "page_subtitle": ("Update your professional certifications." if id else "Add your professional certifications.")
            })


@login_required(login_url="/user/login")
def add_or_edit_social_link(request, id=None):
    profile = request.user.profile
    social_link = None

    if id:
        social_link = get_object_or_404(SocialLink, id=id, profile=profile)

    if request.method == "POST":
        form = SocialLinkForm(request.POST, instance=social_link)
        if form.is_valid():
            link = form.save(commit=False)
            link.profile = profile
            link.save()
            messages.success( request, ("Social link updated successfully." if id else "Social link added successfully." ))
            return redirect("profile")
    else:
        form = SocialLinkForm(instance=social_link)

    return render(request, "pages/users/profile_form.html",  {
            "form": form,
            "page_title": "Edit Social Link" if id else "Add Social Link",
            "page_subtitle": ("Update your social or professional links."  if id  else "Add your social or professional links.")
        })


@login_required(login_url="/user/login")
def add_or_edit_project(request, id=None):
    profile = request.user.profile
    project = None

    if id:
        project = get_object_or_404(Project, id=id, profile=profile)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            proj = form.save(commit=False)
            proj.profile = profile
            proj.save()
            messages.success(request,("Project updated successfully."  if id   else "Project added successfully."))
            return redirect("profile")
    else:
        form = ProjectForm(instance=project)

    return render( request, "pages/users/profile_form.html", {
            "form": form,
            "page_title": "Edit Project" if id else "Add Project",
            "page_subtitle": ("Update your project details." if id else "Add your personal or professional projects.")
        })


@login_required(login_url="/user/login")
def delete_experience(request, id):
    profile = request.user.profile
    experience = get_object_or_404(Experience, id=id, profile=profile)
    experience.delete()
    messages.success(request, "Experience deleted successfully.")
    return redirect("profile")

@login_required(login_url="/user/login")
def delete_education(request, id):
    profile = request.user.profile
    education = get_object_or_404(Education, id=id, profile=profile)
    education.delete()
    messages.success(request, "Education deleted successfully.")
    return redirect("profile")

@login_required(login_url="/user/login")
def delete_certification(request, id):
    profile = request.user.profile
    certification = get_object_or_404(Certification, id=id, profile=profile)
    certification.delete()
    messages.success(request, "Certification deleted successfully.")
    return redirect("profile")

@login_required(login_url="/user/login")
def delete_social_link(request, id):
    profile = request.user.profile
    social_link = get_object_or_404(SocialLink, id=id, profile=profile)
    social_link.delete()
    messages.success(request, "Social link deleted successfully.")
    return redirect("profile")

@login_required(login_url="/user/login")
def delete_project(request, id):
    profile = request.user.profile
    project = get_object_or_404(Project, id=id, profile=profile)
    project.delete()
    messages.success(request, "Project deleted successfully.")
    return redirect("profile")

@login_required(login_url="/user/login")
def view_resume(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    user = profile.user
    experience_duration = calculate_total_experience(profile.experiences.all())
    return render( request, "pages/users/resume.html", {"user":user, "profile": profile, "experience_duration": experience_duration})
