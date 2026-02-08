from django.contrib.auth.models import User
from django.db import models
from skills.models import Skill


class Profile(models.Model):
    def generateImagePath(instance, filename):
        return f"users/{instance.user.username}/{filename}"

    class RoleOptions(models.TextChoices):
        Admin = "Admin", "Admin"
        JobSeeker = "Job Seeker", "Job Seeker"
        Recruiter = "Recruiter", "Recruiter"

    class GenderOptions(models.TextChoices):
        Male = "Male", "Male"
        Female = "Female", "Female"
        Others = "Others", "Others"

    class JobTypeOptions(models.TextChoices):
        FullTime = "Full Time", "Full Time"
        PartTime = "Part Time", "Part Time"
        Contract = "Contract", "Contract"
        Intern = "Internship", "Internship"

    class WorkModeOptions(models.TextChoices):
        OnSite = "On-site", "On-site"
        Remote = "Remote", "Remote"
        Hybrid = "Hybrid", "Hybrid"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100, blank=True)
    summary = models.TextField(blank=True)
    address = models.CharField(max_length=50)
    phone = models.CharField( max_length=10)
    nationality = models.CharField( max_length=15, default="Nepal")
    gender = models.CharField( choices=GenderOptions, default=GenderOptions.Male, max_length=6 )
    profile_image = models.ImageField( blank=True, null=True, upload_to=generateImagePath, default="users/default_user.png" )
    dob = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=RoleOptions, default=RoleOptions.JobSeeker)
    skills = models.ManyToManyField(Skill, blank=True, related_name="profiles")
    preferred_location = models.CharField(max_length=100, blank=True)
    preferred_job_type = models.CharField(max_length=50, choices=JobTypeOptions, blank=True)
    preferred_work_mode = models.CharField(max_length=20, choices=WorkModeOptions, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def completion_percentage(self):
        checks = [
            bool(self.position),
            bool(self.summary),
            bool(self.address),
            bool(self.phone),
            bool(self.dob),
            bool(self.profile_image),
            self.skills.exists(),
            self.educations.exists(),
            self.experiences.exists(),
            self.projects.exists(),
            bool(self.preferred_location),
            bool(self.preferred_job_type),
            bool(self.preferred_work_mode),
        ]

        completed = sum(checks)
        total = len(checks)

        return int((completed / total) * 100)

    def __str__(self):
        return f"{self.user.username}"

class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="experiences")
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="educations")
    institution_name = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} from {self.institution_name}"
    
class Certification(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="certifications")
    name = models.CharField(max_length=100)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} from {self.issuing_organization}"
    
class SocialLink(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="social_links")
    platform = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return f"{self.platform} link for {self.profile.user.username}"

class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=100)
    description = models.TextField()
    project_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} project for {self.profile.user.username}"