from django.http import HttpResponse
from django.core.mail import send_mail


def send_email(request):

    send_mail('Titulo', 'Mensagem', 'teste@teste.com', ['teste2@teste.com'])

    return HttpResponse('email enviado!')
