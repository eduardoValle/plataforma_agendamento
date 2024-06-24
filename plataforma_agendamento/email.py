from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from plataforma_agendamento.settings import EMAIL_HOST_USER, APP_NAME
from register.models import CustomUser


def send_email(recipient_list, message, dados):
    msg_plain = render_to_string('templates/email.txt', {'some_params': dados})
    msg_html = render_to_string('templates/email.html', {'some_params': dados})

    send_mail('email title',
              msg_plain,
              EMAIL_HOST_USER,
              recipient_list,
              html_message=msg_html)


def send_email_appointment_confirmation(url, appointment_serializer):
    try:
        user_id = appointment_serializer['user']
        custom_user = CustomUser.objects.get(pk=user_id)

        print(custom_user.email)

        context = {
            'app_name': APP_NAME,
            'email': [custom_user.email],
            'appointments_service': appointment_serializer['service'],
            'link': '{}/confirm/{}'.format(url, appointment_serializer['token'])
        }

        # render email text
        email_html_message = render_to_string('email/appointments_confirm.html', context)
        email_plaintext_message = render_to_string('email/appointments_confirm.txt', context)

        msg = EmailMultiAlternatives(
            # title:
            "Recuperação de senha para a {title}".format(title=APP_NAME),
            # message:
            email_plaintext_message,
            # from:
            EMAIL_HOST_USER,
            # to:
            [custom_user.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()

    except CustomUser.DoesNotExist:
        print('E-mail de confirmação não enviado, pois não encontramos o usuário {}!'.format(appointment_serializer['user']))
