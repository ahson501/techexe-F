from django.urls import path
from .views import BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView

urlpatterns = [
    path('', BlogPostListView.as_view(), name='Technology'),
    path('post/<int:pk>/', BlogPostDetailView.as_view(), name='blogpost-detail'),
]
