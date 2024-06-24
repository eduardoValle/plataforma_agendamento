


import os

import django
from celery import Celery

from plataforma_agendamento import settings

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataforma_agendamento.settings')
# django.setup()
# app = Celery('plataforma_agendamento', broker='pyamqp://guest@localhost//')
#
# app.autodiscover_tasks()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataforma_agendamento.settings')
app = Celery('plataforma_agendamento')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
