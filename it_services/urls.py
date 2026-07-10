# it_services/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Placeholder paths for our newly created forms
    path('complaint/raise/', views.RaiseComplaintView.as_view(), name='raise_complaint'),
    path('email/apply/', views.ApplyEmailView.as_view(), name='apply_email'),
    path('zoom/register/', views.RegisterZoomView.as_view(), name='register_zoom'),
]