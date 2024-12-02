from django.urls import path
from . import views

app_name = 'AAPlants'  # This is important to use this app's namespace

urlpatterns = [
    path('', views.home, name='aaplantshome'),
    path('catalog/', views.catalog, name='aaplantscatalog'),
    path('category/<slug:category_slug>/', views.category_view, name='aaplantscategory'),
    path('plant/<int:plant_id>/', views.plant_detail, name='aaplants_detail'),
    path('about/', views.about, name='aaplantsabout'),
    path('contact/', views.contact, name='aaplantscontact'),
]
