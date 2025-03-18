from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),  # Include accounts app URLs
    path('api/inventory/', include('inventory.urls')),
    path('api/pos/', include('pos.urls')),
    path('api/suppliers/', include('suppliers.urls')),
    path('api/categories/', include('categories.urls')),
]