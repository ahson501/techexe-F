from django.urls import path
from .views import PortfolioListView, PortfolioDetailView, PortfolioCreateView, PortfolioUpdateView, PortfolioDeleteView, PortfolioAboutView, ContactMeView, ConfirmView, TemplateView
 

urlpatterns = [
    path('', PortfolioListView.as_view(), name='portfolio_list'),
    path('portfolio/<int:pk>/', PortfolioDetailView.as_view(), name='portfolio_detail'),
    path('portfolio/create/', PortfolioCreateView.as_view(), name='portfolio_create'),
    path('portfolio/<int:pk>/update/', PortfolioUpdateView.as_view(), name='portfolio_update'),
    path('portfolio/<int:pk>/delete/', PortfolioDeleteView.as_view(), name='portfolio_delete'),
    path('about/', PortfolioAboutView.as_view(), name='about_me'),
    path('contact_me/', ContactMeView.as_view(), name='contact_me'),
    path('send-email/', ConfirmView.as_view(), name='send_email'),
    path('success/', TemplateView.as_view(template_name='success.html'), name='success'),  # Success page
]
