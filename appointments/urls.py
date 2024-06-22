from django.urls import path

from . import views

urlpatterns = [
    path('', views.findAll, name='all-appointments'),
]
