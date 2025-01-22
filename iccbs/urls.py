from django.urls import path
from . import views  # Import the views module
from .views import RegisterView, PasswordResetView, PasswordChangeView, iccbsView
from django.contrib.auth import views as auth_views

app_name = 'iccbs'  # To namespace the URLs

urlpatterns = [
    path('', views.iccbs_base, name='iccbs_base'),  # Base page (renders base.html)
    path('home/', views.iccbshome, name='iccbshome'),  # Home page (renders iccbshome.html)
    path('register/', RegisterView.as_view(), name='iccbs_register'),  # User registration
    path('password-reset/', PasswordResetView.as_view(), name='iccbs_password_reset'),  # Password reset
    path('login/', auth_views.LoginView.as_view(template_name='iccbs/login.html'), name='iccbs_login'),  # Login
    path('logout/', auth_views.LogoutView.as_view(), name='iccbs_logout'),  # Logout
    path('profile/', views.profile, name='iccbs_profile'),  # Profile page
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),  # Password change
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='iccbs/password_reset_complete.html'),
        name='password_reset_complete'
    ),  # Password reset complete
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='iccbs/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),  # Password reset confirmation
    path('template/', iccbsView.as_view(), name='iccbs_template'),  # Class-based view for iccbs template
]
