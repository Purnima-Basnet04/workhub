from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job
from .forms import JobForm
from skills.models import Skill
from django.db.models import Q

@login_required(login_url='/user/login')
def job_list(request):
    jobs = Job.objects.filter(is_active=True)
    search = request.GET.get('search', '').strip()
    if search:
        jobs = jobs.filter(
            Q(title__icontains=search) |
            Q(company__name__icontains=search) |
            Q(description__icontains=search) |
            Q(location__icontains=search)
        )
    location = request.GET.get('location', '').strip()
    if location:
        jobs = jobs.filter(location__icontains=location)
    company_detail = request.GET.get('company', '').strip()
    if company_detail:
        jobs = jobs.filter(Q(company__public_url=company_detail) | Q(company__name__icontains=company_detail))
    employment_type = request.GET.get('employment_type', '').strip()
    if employment_type:
        jobs = jobs.filter(employment_type=employment_type)
    work_mode = request.GET.get('work_mode', '').strip()
    if work_mode:
        jobs = jobs.filter(work_mode=work_mode)
    min_experience = request.GET.get('min_experience', '').strip()
    if min_experience:
        try:
            min_exp_value = int(min_experience)
            jobs = jobs.filter(min_experience__lte=min_exp_value)
        except ValueError:
            pass  
    min_salary = request.GET.get('min_salary', '').strip()
    if min_salary:
        try:
            min_sal_value = int(min_salary)
            jobs = jobs.filter(Q(salary_min__gte=min_sal_value) | Q(salary_min__isnull=True))
        except ValueError:
            pass
    max_salary = request.GET.get('max_salary', '').strip()
    if max_salary:
        try:
            max_sal_value = int(max_salary)
            jobs = jobs.filter( Q(salary_max__lte=max_sal_value) | Q(salary_max__isnull=True))
        except ValueError:
            pass
    sort = request.GET.get('sort', 'newest')
    if sort == 'oldest':
        jobs = jobs.order_by('created_at')
    elif sort == 'salary_high':
        jobs = jobs.order_by('-salary_max', '-salary_min', '-created_at')
    elif sort == 'salary_low':
        jobs = jobs.order_by('salary_min', 'salary_max', '-created_at')
    else:  
        jobs = jobs.order_by('-created_at')
    jobs = jobs.select_related('recruiter').prefetch_related('skills')
    return render(request, "pages/jobs/job_list.html", {'jobs': jobs})

@login_required(login_url='/users/login')
def job_create(request):
    if request.method == "POST":
        form = JobForm(request.POST, user=request.user)
        skills_ids = request.POST.get("skills", "")
        skills_ids = [int(i) for i in skills_ids.split(",") if i.isdigit()]
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            if skills_ids:
                job.skills.set(Skill.objects.filter(id__in=skills_ids))
            messages.success(request, "Job created successfully.")
            return redirect("/jobs")
    else:
        form = JobForm(user=request.user)
    skills = Skill.objects.filter(is_active=True).values("id", "name")
    return render(request, "pages/jobs/create_job.html", {"form": form,"skills": list(skills)})

@login_required(login_url='/users/login')
def job_update(request, pk):
    job = get_object_or_404(Job, pk=pk, recruiter=request.user)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job, user = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully.")
            return redirect("/jobs")
    else:
        form = JobForm(instance=job, user=request.user)
    skills_ids_str = ','.join(str(s.id) for s in job.skills.all())
    skills = Skill.objects.filter(is_active=True).values("id", "name")
    return render(request, "pages/jobs/edit_job.html", {"form": form, "job": job, "skills_ids_str": skills_ids_str, "skills": list(skills)})

@login_required(login_url='/users/login')
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk, recruiter=request.user)
    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect("/jobs")
    return redirect("/jobs")

@login_required(login_url='/users/login')
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, "pages/jobs/job_detail.html", {"job": job})
