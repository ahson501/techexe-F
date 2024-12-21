from django.shortcuts import render, get_object_or_404
from .models import Plant, About, Category, Testimonial, Item
from django.http import JsonResponse
from django_elasticsearch_dsl.search import Search
from .documents import PlantDocument
from elasticsearch import Elasticsearch  # Add this import


# View for the home page
def home(request):
    return render(request, 'aaplantshome.html')

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

# Set up Elasticsearch client

es = Elasticsearch(
    hosts=["http://es:9200"],  # Use 'es' as the hostname
    http_auth=("elastic", "12345678")  # Your credentials
)

def aaplants_search(request):
    query = request.GET.get('q', '')
    if query:
        search = PlantDocument.search().query(
            "multi_match",
            query=query,
            fields=["name", "description", "scientific_name"]
        )
        results = search.execute()
        plants = [
            {
                "name": hit.name,
                "scientific_name": hit.scientific_name,
                "description": hit.description,
                "id": hit.meta.id,
            }
            for hit in results
        ]
        return JsonResponse({"plants": plants})
    return render(request, "aaplants_search.html", {"message": "No search query provided"})
