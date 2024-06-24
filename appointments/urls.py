from django.urls import path

from . import views

urlpatterns = [
    path('', views.appointments, name='appointments'),
    path('/<int:id>', views.appointments_id, name='appointments-id'),
    path('/confirm/<str:token>', views.appointments_confirm, name='appointments-confirm'),
]
