from django.urls import path
from .views import ComplaintListView, ComplaintCreateView, ComplaintUpdateView

urlpatterns = [
    path('', ComplaintListView.as_view(), name='complaint-list'),
    path('new/', ComplaintCreateView.as_view(), name='complaint-create'),
    path('<int:pk>/update/', ComplaintUpdateView.as_view(), name='complaint-update'),
]
