from django.urls import path
from . import views

app_name = 'blog'  # Define the namespace for this app

urlpatterns = [
    path('', views.index, name='index'),  # Map the root URL to the index view
]

