from django.shortcuts import render, get_object_or_404
from .models import Plant, About, Category, Testimonial, Item  # Import the model correctly, matching the model name in 'models.py'
from django.db.models import Q


# View for the home page
def home(request):
    return render(request, 'aaplantshome.html')

def category_list(request):
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'aaplantscategory.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    plants = category.plants.all()  # Use the related name defined in the `Plant` model.
    return render(request, 'aaplantscategory_detail.html', {
    'category': category,
    'plants': plants,
})

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

def aaplants_search(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    results = []  # Initialize an empty list for storing search results

    if query:
        # Perform search across the Plant model
        plant_results = Plant.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        results.extend([{'object': plant, 'model': 'Plant'} for plant in plant_results])

        # Perform search across the About model
        about_results = About.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        results.extend([{'object': about, 'model': 'About'} for about in about_results])

        # Perform search across the Category model
        category_results = Category.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        results.extend([{'object': category, 'model': 'Category'} for category in category_results])

        # Perform search across the Testimonial model
        testimonial_results = Testimonial.objects.filter(
            Q(name__icontains=query) | Q(content__icontains=query)
        )
        results.extend([{'object': testimonial, 'model': 'Testimonial'} for testimonial in testimonial_results])

        # Perform search across the Item model
        item_results = Item.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        results.extend([{'object': item, 'model': 'Item'} for item in item_results])

    # Render the template with the query and search results
    return render(request, 'aaplants_search.html', {
        'query': query,
        'results': results,
    })
