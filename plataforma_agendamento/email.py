from django.core.mail import send_mail
from django.template.loader import render_to_string

from plataforma_agendamento.settings import EMAIL_HOST_USER


def send_email(recipient_list, message, dados):
    msg_plain = render_to_string('templates/email.txt', {'some_params': dados})
    msg_html = render_to_string('templates/email.html', {'some_params': dados})

    send_mail('email title',
              msg_plain,
              EMAIL_HOST_USER,
              recipient_list,
              html_message=msg_html)
