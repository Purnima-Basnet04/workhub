from django.urls import path
from .views import apply_job, cancel_application, application_list

urlpatterns = [
    path("apply/<int:job_id>/", apply_job, name="apply_job"),
    path("cancel/<int:job_id>/", cancel_application, name="cancel_application"),
    path("", application_list, name="application_list"),
]
