from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def landingPage(request):
    return render(request, "pages/index.html")

@login_required(login_url='/users/login')
def dashboard(request):
    return render(request, 'pages/dashboard/jdashboard.html')
