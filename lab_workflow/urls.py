# lab_workflow/urls.py
from django.urls import path
from . import views

app_name = 'lab_workflow'

urlpatterns = [
    # Landing page service hub route
    path('service-hub/', views.service_hub, name='service_hub'),
    path('post-login-redirect/', views.post_login_redirect, name='post_login_redirect'),
    path('sop/', views.sop_gate, name='sop_gate'),
    path('dashboard/', views.dashboard, name='lab_dashboard'),
    # This is techexe.net/lab_workflow/uplc-form/
    path("uplc-form/", views.uplc_form_view, name="uplc_form"),
    path('nmr-form/', views.nmr_form_view, name='nmr_form'),
    path('request/<int:pk>/', views.uplc_detail, name='uplc_detail'),
    path('nmr/<int:pk>/', views.nmr_detail, name='nmr_detail'),
    # Approval actions
    path("approve/<int:pk>/", views.approve_request, name="approve_request"),
    path('reject-tlc/<str:request_type>/<int:pk>/', views.reject_invalid_tlc, name='reject_tlc'),
    path("reject/<int:pk>/", views.reject_request, name="reject_request"),
    path('print/<str:request_type>/<int:pk>/', views.print_form, name='print_form'),
    path('ajax/ai-query/', views.route_ai_query, name='ai_query_route'),
    # AI-agent
    path("api/ai-query/", views.route_ai_query, name="route_ai_query"),
    path("api/agents-query/", views.route_agents_query, name="route_agents_query"),
    path('uploads', views.proxy_uploads, name='proxy_uploads'),
]