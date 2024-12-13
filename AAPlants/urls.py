from django.urls import path
from . import views

app_name = 'AAPlants'  # This is important to use this app's namespace

urlpatterns = [
    path('', views.home, name='aaplantshome'),
    path('category/', views.category_list, name='aaplantscategory'),
    path('category/<slug:category_slug>/', views.category_detail, name='aaplantscategory_detail'),
    path('plant/<int:plant_id>/', views.plant_detail, name='aaplants_detail'),
    path('about/', views.about, name='aaplantsabout'),
    path('contact/', views.contact, name='aaplantscontact'),
    path('search/', views.aaplants_search, name='aaplants_search'),  
]
