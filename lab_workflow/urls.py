# lab_workflow/urls.py
from django.urls import path
from .views import nmr_form_view, uplc_form_view, dashboard, approve_request, reject_request, request_detail, nmr_detail
from lab_workflow.views import post_login_redirect

app_name = 'lab_workflow'

urlpatterns = [
    # This is techexe.net/lab_workflow/ 
    path('post-login-redirect/', post_login_redirect, name='post_login_redirect'),
    path('dashboard/', dashboard, name='lab_dashboard'),
    # This is techexe.net/lab_workflow/uplc-form/
    path("uplc-form/", uplc_form_view, name="uplc_form"),
    path('nmr-form/', nmr_form_view, name='nmr_form'),
    path('request/<int:pk>/', request_detail, name='request_detail'),
    path('nmr/<int:pk>/', nmr_detail, name='nmr_detail'),
    # Approval actions
    path("approve/<int:pk>/", approve_request, name="approve_request"),
    path("reject/<int:pk>/", reject_request, name="reject_request"),
]