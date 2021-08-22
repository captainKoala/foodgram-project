from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('website.urls'), name='website'),
    path('', include('api.urls'), name='api'),
    path('', include('users.urls'), name='users'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,
    )
