from celery import shared_task
from celery.utils.log import get_task_logger

from plataforma_agendamento.email import send_email_appointment_confirmation
from register.models import CustomUser

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=5, default_retry_delay=30)
def send_appointment_confirmation_email_task(self, url, appointment_serializer, *ext_args, **kwarg):
    try:
        user_id = appointment_serializer['user']
        print(user_id)
        mensagem = 'Enviando e-mail de confirmação de agendamento!'
        custom_user = CustomUser.objects.get(pk=user_id)

        logger.info(mensagem)
        send_email_appointment_confirmation(url, appointment_serializer, custom_user.email)
        return True

    except CustomUser.DoesNotExist:
        print('E-mail de confirmação não enviado, pois não encontramos o usuário {}!'.format(appointment_serializer['user']))

    except Exception as e:
        print(e)


    # return send_email(recipient_list, message, review)
