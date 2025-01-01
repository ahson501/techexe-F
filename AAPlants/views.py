from django.shortcuts import render, get_object_or_404, redirect
from .models import Plant, About, Category, Testimonial, Item
from django.db import connection  # Add this import
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm



# View for the home page
def home(request):
    return render(request, 'aaplantshome.html', {'on_homepage': True})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'aaplantscategory.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render(request, 'aaplantscategory_detail.html', {'category': category})

# View for individual plant details
def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    return render(request, 'aaplants_detail.html', {'plant': plant})

# View for the "About Us" page
def about(request):
    return render(request, 'aaplantsabout.html')

# View for a custom contact page
def contact(request):
    return render(request, 'aaplantscontact.html')

def aaplants_search(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        # Adjust the query to use category_id instead of category
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, scientific_name, description, care_instructions, category_id
                FROM "AAPlants_plant"
                WHERE name ILIKE %s
                OR scientific_name ILIKE %s
                OR description ILIKE %s
                OR care_instructions ILIKE %s
                OR category_id::text ILIKE %s  -- Assuming category_id is an integer and we are converting it to text
                """, 
                [f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"]
            )
            results = cursor.fetchall()

    return render(request, "aaplants_search.html", {"results": results, "query": query})

@login_required
def user_details(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile view after saving
    else:
        form = CustomLoginForm(instance=request.user)
    return render(request, 'user_details.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})