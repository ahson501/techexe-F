from django.shortcuts import render


def home(request):
    return render(request, 'home.html')

def services(request):
    return render(request, 'services.html')

def technology(request):
    return render(request, 'technology.html')

def docker_login(request):
    return render(request, 'docker_login.html')

def ai_tutor(request):
    return render(request, 'ai_tutor.html')

def about(request):
    return render(request, 'about.html')
