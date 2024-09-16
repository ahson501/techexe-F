from django.shortcuts import render
from .models import Project


def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

def index(request):
    return render(request, 'index.html')  # Create an index.html file to render

def about(request):
    return render(request, 'about.html') 