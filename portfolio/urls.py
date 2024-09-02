from django.urls import path
from . import views

app_name = 'portfolio'  # Define the namespace for this app

urlpatterns = [
    path('', views.index, name='portfolio_list'),
    # Define other URL patterns for the portfolio app here
]
