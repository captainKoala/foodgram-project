from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls'), name='api'),
    path('api/', include('users.urls'), name='users'),
]
