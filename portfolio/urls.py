from django.urls import path
from .views import PortfolioListView, PortfolioDetailView, PortfolioCreateView, PortfolioUpdateView, PortfolioDeleteView

urlpatterns = [
    path('', PortfolioListView.as_view(), name='portfolio_list'),
    path('portfolio/<int:pk>/', PortfolioDetailView.as_view(), name='portfolio_detail'),
    path('portfolio/create/', PortfolioCreateView.as_view(), name='portfolio_create'),
    path('portfolio/<int:pk>/update/', PortfolioUpdateView.as_view(), name='portfolio_update'),
    path('portfolio/<int:pk>/delete/', PortfolioDeleteView.as_view(), name='portfolio_delete'),
]