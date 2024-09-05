from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Portfolio

class PortfolioListView(ListView):
    model = Portfolio
    template_name = 'portfolio_list.html'
    context_object_name = 'object_list'

class PortfolioDetailView(DetailView):
    model = Portfolio
    template_name = 'portfolio_detail.html'
    context_object_name = 'portfolio'

class PortfolioCreateView(CreateView):
    model = Portfolio
    template_name = 'portfolio_form.html'
    fields = ['title', 'image', 'description', 'technology', 'date_pub']
    success_url = reverse_lazy('portfolio_list')

class PortfolioUpdateView(UpdateView):
    model = Portfolio
    template_name = 'portfolio_form.html'
    fields = ['title', 'image', 'description', 'technology', 'date_pub']
    success_url = reverse_lazy('portfolio_list')

class PortfolioDeleteView(DeleteView):
    model = Portfolio
    template_name = 'portfolio_confirm_delete.html'
    success_url = reverse_lazy('portfolio_list')
