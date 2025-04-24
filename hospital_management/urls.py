from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# configuring swagger 
schema_view = get_schema_view(
    openapi.Info(
        title="Medic Plus Backend",
        default_version='v1',
        description="API documentation for Medic Plus",
        terms_of_service="",
        contact=openapi.Contact(email="eriddeveloper@gmail.com"),
        license=openapi.License(name="My License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),  # Include accounts app URLs
    path('api/inventory/', include('inventory.urls')),
    path('api/pos/', include('pos.urls')),
    path('api/suppliers/', include('suppliers.urls')),
    path('api/categories/', include('categories.urls')),
    path('api/products/', include('products.urls')),

    # Swagger URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]