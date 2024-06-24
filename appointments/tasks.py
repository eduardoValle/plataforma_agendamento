from celery import shared_task
from celery.utils.log import get_task_logger

from plataforma_agendamento.email import send_email_appointment_confirmation
from register.models import CustomUser

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=5, default_retry_delay=30)
def send_appointment_confirmation_email_task(self, url, appointment_serializer, *ext_args, **kwarg):
    try:
        logger.info('Enviando e-mail de confirmação de agendamento!')
        send_email_appointment_confirmation(url, appointment_serializer)
        return True

    except Exception as e:
        print(e)
