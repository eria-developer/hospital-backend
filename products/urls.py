from django.urls import path
from .views import (
    ProductListCreateView,
    ProductDetailView,
    ProductStockUpdateView,
    ProductImageCreateView
)

app_name = 'inventory'

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/stock/', ProductStockUpdateView.as_view(), name='product-stock-update'),
    path('<int:pk>/images/', ProductImageCreateView.as_view(), name='product-image-create'),
]