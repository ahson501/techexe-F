from django.urls import path
from . import views

app_name = 'home'  # To namespace the URLs

urlpatterns = [
    path('', views.home, name='home'),  # Home page URL pattern
    path('services/', views.services, name='services'),
    path('technology/', views.technology, name='technology'),
    path('docker-login/', views.docker_login, name='docker_login'),
    path('ai-tutor/', views.ai_tutor, name='ai_tutor'),
    path('about/', views.about, name='about'),
]
