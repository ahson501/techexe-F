# blog/views.py

from django.shortcuts import render
from .models import Index  # Use the correct model class name

# Define the index view
def index(request):
    posts = Index.objects.all()  # Fetch all blog posts using the 'Index' model
    return render(request, 'blog/index.html', {'posts': posts})  # Render the 'index.html' template with the posts
