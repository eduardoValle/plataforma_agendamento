from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/register', include('register.urls')),
    path('api/appointments', include('appointments.urls')),

    path('', include('pages.urls')),
    path('login', include('authentication.urls')),
]
