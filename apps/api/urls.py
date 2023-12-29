from django.urls import path, include
from .views import index
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# Root level urls for switching between diffrent implementations of APIs

urlpatterns = [
    path('', index),
    path('v1/', include("apps.api.vers.v1.urls")),
    path('auth/', include("apps.api.auth.urls")),

    # API Specs
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
