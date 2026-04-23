# lab_workflow/urls.py
from django.urls import path
from .views import uplc_form_view, dashboard, approve_request, reject_request, request_detail

urlpatterns = [
    # This is techexe.net/lab_workflow/
    path("", dashboard, name="dashboard"), 
    #path("dashboard/", dashboard, name="dashboard"),
    
    # This is techexe.net/lab_workflow/uplc-form/
    path("uplc-form/", uplc_form_view, name="uplc_form"),
    path('request/<int:pk>/', request_detail, name='request_detail'),
    # Approval actions
    path("approve/<int:pk>/", approve_request, name="approve_request"),
    path("reject/<int:pk>/", reject_request, name="reject_request"),
]