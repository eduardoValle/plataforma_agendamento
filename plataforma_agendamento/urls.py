from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from plataforma_agendamento.settings import EMAIL_HOST_USER, APP_NAME, APP_DESCRIPTION

schema_view = get_schema_view(
    openapi.Info(
        title=APP_NAME,
        default_version='v1',
        description=APP_DESCRIPTION,
        license=openapi.License(name="MIT License"),
        contact=openapi.Contact(email=EMAIL_HOST_USER),
        terms_of_service="https://github.com/eduardoValle/plataforma_agendamento",
    ),
    public=True,
    # permission_classes=(permissions.AllowAny)
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('api.urls')),
    path('api/register', include('register.urls')),
    path('api/appointments', include('appointments.urls')),

    path('api/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
