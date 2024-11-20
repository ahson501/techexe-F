from django.urls import path
from .views import BlogPostListView, BlogPostDetailView, CategoryListView

urlpatterns = [
    path('', BlogPostListView.as_view(), name='blogpost_list'),  # List of all blog posts
    path('category/<slug:category_slug>/', BlogPostListView.as_view(), name='category_blogpost_list'),
    path('<slug:slug>/', BlogPostDetailView.as_view(), name='blogpost_detail'),  # Detail view for a single blog post using slug
    path('categories/', CategoryListView.as_view(), name='category_list'),  # List of categories
]
