from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Portfolio, ContactInfo
from django.shortcuts import render



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

class PortfolioAboutView(TemplateView):
    model = Portfolio
    template_name = 'about_me.html'
    success_url = reverse_lazy('portfolio_list')

class ContactMeView(TemplateView):
    template_name = 'contact_me.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Assuming there's only one ContactInfo instance
        contact_info = ContactInfo.objects.first()
        context['info'] = contact_info
        return context

def portfolio_list(request):
    info = {
        'about': "I am a software developer with experience in Django and Docker...",
        'phone': "123-456-7890",
        'email': "your-email@example.com",
        'github': "https://github.com/yourprofile",
        'linkedin': "https://linkedin.com/in/yourprofile",
        'instagram': "https://instagram.com/yourprofile",
        'facebook': "https://facebook.com/yourprofile",
        'twitter': "https://twitter.com/yourprofile"
    }
    return render(request, 'portfolio_list.html', {'info': info, 'object_list': PortfolioListView})   