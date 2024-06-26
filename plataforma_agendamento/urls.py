from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
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

token_response = openapi.Response(
    'Objeto utilizado para resposta de autenticação. Contém um par de Json Web Tokens, um de "access" e um "refresh".',
    TokenRefreshSerializer)

decorated_login_view = \
    swagger_auto_schema(method='post', request_body=TokenObtainPairSerializer, responses={200: token_response},
                        operation_description='Recebe um conjunto de credenciais de usuário e retorna um par de Json Web Tokens, um de "access" e um "refresh", para provar a autenticação do usuário.'
                        )(TokenObtainPairView.as_view())

decorated_token_refresh_view = \
    swagger_auto_schema(method='post', request_body=TokenObtainPairSerializer, responses={200: token_response},
                        operation_description='Recebe um Json Web Token do tipo de "refresh" válido e retorna um objeto do tipo TokenRefresh.'
                        )(TokenRefreshView.as_view())

password_reset_view = \
    swagger_auto_schema(method='post', request_body=TokenObtainPairSerializer, responses={200: token_response},
                        operation_description='Recebe um Json Web Token do tipo de "refresh" válido e retorna um objeto do tipo TokenRefresh.'
                        )(TokenRefreshView.as_view())

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('api.urls')),
    path('api/register', include('register.urls')),
    path('api/appointments', include('appointments.urls')),

    path('api/login', decorated_login_view, name='token_obtain_pair'),
    path('api/token/refresh', decorated_token_refresh_view, name='token_refresh'),
    path('api/password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
