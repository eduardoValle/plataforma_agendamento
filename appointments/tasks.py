from celery import shared_task
from celery.utils.log import get_task_logger

from appointments.models import Appointment
from plataforma_agendamento.email import send_email_appointment_confirmation

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=5, default_retry_delay=30)
def execute_appointments_service(self, appointment_id, *ext_args, **kwarg):
    try:
        appointment = Appointment.objects.get(pk=appointment_id)
        appointment.execute()
        return True

    except Exception as e:
        print(e)
        self.retry(countdown=5, exec=e)


@shared_task(bind=True, max_retries=5, default_retry_delay=30)
def send_appointment_confirmation_email_task(self, url, appointment_serializer, *ext_args, **kwarg):
    try:
        logger.info('Enviando e-mail de confirmação de agendamento!')
        send_email_appointment_confirmation(url, appointment_serializer)
        return True

    except Exception as e:
        print(e)
        self.retry(countdown=5, exec=e)
