from django.shortcuts import render
from django.views.generic import ListView
from .models import Plant

def plant_home(request):
    # Optionally, you can fetch some general plant details to display on the homepage
    plants = Plant.objects.all()  # Fetch all plants (or any specific query you need)
    return render(request, 'plant_home.html', {'plants': plants})  # Render home.html template
class PlantListView(ListView):
    model = Plant
    template_name = 'plant_list.html'
    context_object_name = 'plants'  # Name the context variable to be used in the template