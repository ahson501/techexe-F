from django.shortcuts import render, get_object_or_404
from .models import Plant  # Import the model correctly, matching the model name in 'models.py'

# View for the home page
def home(request):
    return render(request, 'aaplantshome.html')

# View for the plants catalog
def catalog(request):
    return render(request, 'aaplantscatalog.html')

# View for individual plant details
def plant_detail(request, plant_id):
    # Fetch plant details using `plant_id`
    plant = get_object_or_404(Plant, id=plant_id)  # Use the correct model name (Plant)
    return render(request, 'aaplants_detail.html', {'plant': plant})

# View for the "About Us" page
def about(request):
    return render(request, 'aaplantsabout.html')

# View for a custom contact page
def contact(request):
    return render(request, 'aaplantscontact.html')
