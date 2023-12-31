from django.urls import path, include
from .views import index
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# Root level urls for switching between diffrent implementations of APIs

urlpatterns = [
    path('', index),
    path('v1/', include("apps.api.vers.v1.urls"), name='Purchase Order APIs v1'),
    path('auth/', include("apps.api.auth.urls"), name='Token Based Authentication APIs v1'),

    # API Specs
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
