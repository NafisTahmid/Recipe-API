from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name="api-schema"),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name="api-schema"), name="api-docs"),
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api/user/', include('user.urls')),
    path('api/recipe/', include('recipe.urls'))
]
