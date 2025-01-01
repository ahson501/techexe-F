from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'AAPlants'  # This is important to use this app's namespace

urlpatterns = [
    path('', views.home, name='aaplantshome'),
    path('category/', views.category_list, name='aaplantscategory'),
    path('category/<slug:slug>/', views.category_detail, name='aaplantscategory_detail'),
    path('plant/<int:plant_id>/', views.plant_detail, name='aaplants_detail'),
    path('about/', views.about, name='aaplantsabout'),
    path('contact/', views.contact, name='aaplantscontact'),
    path('search/', views.aaplants_search, name='aaplants_search'), 
    path('user-details/', views.user_details, name='user_details'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),

]
