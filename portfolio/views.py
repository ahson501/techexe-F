from django.shortcuts import render

# View for the portfolio index page
def index(request):
    return render(request, 'portfolio/index.html')


