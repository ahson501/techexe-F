from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import BlogPost

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blogpost_list.html'  # Specify your template here
    context_object_name = 'blogposts'
    ordering = ['-date_created']  # Order by newest first

# Detail view to display a single blog post
class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blogpost_detail.html'  # Specify your template here
    context_object_name = 'blogpost'

# Create view to allow adding new blog posts
class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = 'blogpost_form.html'
    fields = ['title', 'content']  # Include fields you want to display in form

# Update view to allow editing an existing blog post
class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blogpost_form.html'
    fields = ['title', 'content']

# Delete view to delete a blog post
class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blogpost_confirm_delete.html'
    success_url = reverse_lazy('blogpost-list')  # Redirect to list view after deletion
