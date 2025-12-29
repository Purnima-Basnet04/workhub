from django.contrib.auth.models import User
from django.db import models
from skills.models import Skill


class Profile(models.Model):
    def generateImagePath(instance, filename):
        return f"users/{instance.user.username}/{filename}"

    class RoleOptions(models.TextChoices):
        Admin = "admin", "Admin"
        JobSeeker = "jobseeker", "Job Seeker"
        Recruiter = "recruiter", "Recruiter"

    class GenderOptions(models.TextChoices):
        Male = "Male", "Male"
        Female = "Female", "Female"
        Others = "Others", "Others"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    phone = models.CharField( max_length=10)
    nationality = models.CharField( max_length=15, default="Nepal")
    gender = models.CharField( choices=GenderOptions, default=GenderOptions.Male, max_length=6 )
    profile_image = models.ImageField( blank=True, null=True, upload_to=generateImagePath, default="users/default_user.png" )
    dob = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=RoleOptions, default=RoleOptions.JobSeeker)
    skills = models.ManyToManyField(Skill, blank=True, related_name="profiles")
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    preferred_location = models.CharField(max_length=100, blank=True)
    preferred_job_type = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"
