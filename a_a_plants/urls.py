from django.urls import path
from .views import PlantListView, plant_home  # Import both views

urlpatterns = [
    path('', plant_home, name='plant_home'),  # This will be your homepage
    path('plants/', PlantListView.as_view(), name='plant_list'),  # List view for plant details
]
