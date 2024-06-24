from celery import shared_task
from celery.utils.log import get_task_logger

from plataforma_agendamento.email import send_email

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=5, default_retry_delay=30)
def send_appointment_confirmation_email_task(self, recipient_list, message, review):
    try:
        logger.info(message)
        print('Started task, processing...')
        # time.sleep(10)
        print('Finished Task')
        send_email(recipient_list, message, review)
        # send_email('Titulo', '*****************  Mensagem ********************',
        #           'luizeduardovalle@gmail.com', ['luizeduardovalle@gmail.com'])
        return True

    except Exception as e:
        print(e)


    # return send_email(recipient_list, message, review)
