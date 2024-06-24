import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer
from appointments.tasks import send_appointment_confirmation_email_task, execute_appointments_service


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated])
def appointments(request):
    """
    Retorna uma lista todos os Appointments registrados. [Precisa estar auntenticado!]
    """

    # RETORNANDO LISTA DE OBJETOS
    if request.method == 'GET':
        Appointment.objects.all()
        serializer = AppointmentSerializer(Appointment.objects.all(), many=True)
        return Response(serializer.data)


    """
    Insere um novo objeto do tipo Appointment na base de dados. [Precisa estar auntenticado!]
    """
    # INSERINDO NOVO OBJETO
    if request.method == 'POST':
        request.data['status'] = 'pending'
        request.data['token'] = uuid.uuid1().hex
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            url = request.build_absolute_uri(reverse('appointments'))
            send_appointment_confirmation_email_task.delay(url, serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Atualiza um objeto existente do tipo Appointment na base dedados. [Precisa estar auntenticado!]
    """
    # ATUALIZANDO OBJETO
    if request.method == 'PUT':
        try:
            id = request.data['id']
            appointment = Appointment.objects.get(pk=id)
            serializer = AppointmentSerializer(appointment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def appointments_id(request, id):

    """
    Retorna um objeto existente do tipo Appointment que tem o id igual ao informado. [Precisa estar auntenticado!]

    :param id: Atributo id referente ao objeto Appointment.
    :return: objeto do tipo Appointment
    """
    if request.method == 'GET':
        try:
            appointment = Appointment.objects.get(pk=id)
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data)

        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    """
    Remove um objeto existente do tipo Appointment que tem o id igual ao informado. [Precisa estar auntenticado!]
    """
    if request.method == 'DELETE':
        try:
            appointment = Appointment.objects.get(pk=id)
            appointment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def appointments_confirm(request, token):
    """
    Altera o status de um Appointment de 'Pending' pora 'Confirmed'. Em seguida o coloca na fila de processamentod o Celery.
    """

    if request.method == 'GET':
        try:
            appointment = Appointment.objects.get(token=token)

            # if timezone.now < appointment.date:
            #     return Response('Não foi possível confirmar o serviço, pois sua data já passou!')

            appointment.status = 'Confirmed'
            appointment.save()
            execute_appointments_service.delay(appointment.id)
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
