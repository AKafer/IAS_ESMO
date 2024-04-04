from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from api.urls import urlpatterns as api_routes

urlpatterns = [
    # path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
]

urlpatterns.extend(api_routes)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


