from django.http import HttpResponse
from django.core.mail import send_mail

from plataforma_agendamento.settings import EMAIL_HOST


def send_email(request):

    send_mail('Titulo', 'Mensagem', EMAIL_HOST, ['luizeduardovalle@gmail.com'])

    return HttpResponse('email enviado!')
