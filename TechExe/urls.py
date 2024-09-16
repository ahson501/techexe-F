from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),  # This should match your view
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
]


