from django.shortcuts import render, get_object_or_404
from .models import Plant, About, Category, Testimonial, Item  # Import the model correctly, matching the model name in 'models.py'
from django.db.models import Q


# View for the home page
def home(request):
    return render(request, 'aaplantshome.html')

def category_list(request):
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'aaplantscategory.html', {'categories': categories})

def category_detail(request, category_slug):
    # Retrieve the category by slug
    category = get_object_or_404(Category, slug=category_slug)
    # Retrieve items associated with this category
    items = Item.objects.filter(category=category)
    # Render the template with context
    return render(request, 'aaplantscategory_detail.html', {'category': category, 'items': items})

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
    query = request.GET.get('q', '')
    results = []
    if query:
        search_results = Plant.objects.filter(name__icontains=query)  # Update the query logic
        for result in search_results:
            fields = {
                field.name: getattr(result, field.name)
                for field in result._meta.get_fields()
                if not field.many_to_many and not field.one_to_many
            }
            results.append({
                'model': result.__class__.__name__,
                'fields': fields,
            })
    
    return render(request, 'aaplants_search.html', {
        'query': query,
        'results': results,
    })
