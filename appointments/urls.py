from django.urls import path

from . import views

urlpatterns = [
    path('', views.appointments, name='appointments'),
    path('<int:id>', views.appointments_id, name='appointments-id'),
]
