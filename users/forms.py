from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.core.files.uploadedfile import UploadedFile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True, min_length=3, max_length=15)
    first_name = forms.CharField(required=True, min_length=2, max_length=25)
    last_name = forms.CharField(required=True, min_length=2, max_length=25)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "first_name", "last_name" )
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("address", "phone", "nationality", "gender", "profile_image", "dob", "role", "experience", "education", "resume", "preferred_location", "preferred_job_type")

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone:
            if not phone.isdigit() or len(phone) != 10:
                raise forms.ValidationError("Phone number must be 10 digits.")
        return phone

    def clean_profile_image(self):
        img = self.cleaned_data.get("profile_image")
        if not isinstance(img, UploadedFile):
            return img
        if img.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Image size should be less than 5MB.")
        ext = img.name.split(".")[-1].lower()
        if ext not in ("jpg", "jpeg", "png"):
            raise forms.ValidationError("Unsupported image extension.")
        return img
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True, min_length=3, max_length=15)
    first_name = forms.CharField(required=True, min_length=2, max_length=25)
    last_name = forms.CharField(required=True, min_length=2, max_length=25)
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username=username)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if self.instance.pk: 
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This email is already taken.")
        return email

