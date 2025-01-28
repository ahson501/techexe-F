from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'iccbs'  # Namespace for the app

urlpatterns = [
    # Base Page
    path('', views.iccbs_base, name='iccbs_base'),  # Base page (renders base.html)
    
    # Home Page
    path('iccbshome/', views.iccbshome, name='iccbshome'),  # Home page (requires login)
    path('profile/', views.profile, name='profile'), 
    path('profile/<str:username>/', views.public_profile, name='public_profile'),

    # Registration
    path('register/', views.RegisterView.as_view(), name='iccbs_register'),  # User registration
    
    # Login and Logout
    path('login/', views.login_view, name='iccbs_login'),  # Custom login view
    path('logout/', views.logout_view, name='iccbs_logout'),  # Custom logout view
    
    # Password Management
    path('password-reset/', 
         views.ResetPasswordView.as_view(), 
         name='iccbs_password_reset'),  # Password reset
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='iccbs/password_reset_done.html'), 
         name='password_reset_done'),  # Password reset done
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='iccbs/password_reset_confirm.html'), 
         name='password_reset_confirm'),  # Password reset confirm
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='iccbs/password_reset_complete.html'), 
         name='password_reset_complete'),  # Password reset complete
    
    # Password Change
    path('password-change/', 
         views.ResetPasswordView.as_view(), 
         name='password_change'),  # Password change
    path('password-change/done/', 
         auth_views.PasswordChangeDoneView.as_view(template_name='iccbs/password_change_done.html'), 
         name='password_change_done'),  # Password change done
]
