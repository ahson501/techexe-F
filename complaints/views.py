from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from .models import Complaint
from .forms import ComplaintForm
from django.contrib.auth.mixins import LoginRequiredMixin

# ListView for all complaints (for admin)
class ComplaintListView(LoginRequiredMixin, ListView):
    model = Complaint
    template_name = 'complaint_list.html'
    context_object_name = 'complaints'
    login_url = 'login'

    def get_queryset(self):
        # Admin can see all complaints, users only see their own complaints
        if self.request.user.is_staff:
            return Complaint.objects.all()
        else:
            return Complaint.objects.filter(user=self.request.user)

# CreateView for submitting a complaint
class ComplaintCreateView(LoginRequiredMixin, CreateView):
    model = Complaint
    form_class = ComplaintForm
    template_name = 'complaint_form.html'
    success_url = reverse_lazy('complaint-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# UpdateView for changing status of a complaint (admin only)
class ComplaintUpdateView(LoginRequiredMixin, UpdateView):
    model = Complaint
    fields = ['status']
    template_name = 'complaint_status_update.html'
    success_url = reverse_lazy('complaint-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('complaint-list')
        return super().dispatch(request, *args, **kwargs)
    
