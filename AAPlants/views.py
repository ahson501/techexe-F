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
    query = request.GET.get('q', '')  # Get the search query
    results = []  # Initialize an empty list for storing search results

    if query:
        models_to_search = [Plant, About, Category, Testimonial, Item]  # Add all your models here

        for model in models_to_search:
            fields = [field.name for field in model._meta.fields if field.get_internal_type() in ['CharField', 'TextField']]
            queries = Q()

            # Dynamically search across all CharField and TextField fields
            for field in fields:
                queries |= Q(**{f"{field}__icontains": query})

            # Fetch results for the current model
            model_results = model.objects.filter(queries)
            results.extend([{'object': obj, 'model': model.__name__} for obj in model_results])

    return render(request, 'aaplants_search.html', {
        'query': query,
        'results': results,
    })