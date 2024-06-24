import time

from celery import shared_task
from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework.response import Response


def send_email(request):
    send_mail('Titulo', '*****************  Mensagem ********************',
              'luizeduardovalle@gmail.com', ['luizeduardovalle@gmail.com'])
    # slow_task.delay()
    return HttpResponse('email enviado!')


# @shared_task(queue='default')
@shared_task(bind=True, max_retries=5, default_retry_delay=30)
def slow_task(self):
    try:
        print('Started task, processing...')
        time.sleep(10)
        print('Finished Task')
        send_mail('Titulo', '*****************  Mensagem ********************',
                  'luizeduardovalle@gmail.com', ['luizeduardovalle@gmail.com'])
        return True

    except Exception as e:
        print(e)
        self.retry(countdown=5, exec=e)
