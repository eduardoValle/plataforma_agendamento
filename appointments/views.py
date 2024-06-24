from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer
from appointments.tasks import send_appointment_confirmation_email_task


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated])
def appointments(request):
    # RETORNANDO LISTA DE OBJETOS
    if request.method == 'GET':
        Appointment.objects.all()
        serializer = AppointmentSerializer(Appointment.objects.all(), many=True)
        return Response(serializer.data)

    # INSERINDO NOVO OBJETO
    if request.method == 'POST':
        request.data['status'] = 'pending'
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_appointment_confirmation_email_task.delay(['djangoagendamento@gmail.com'],
                                                           'Enviando e-mail de confirmação de agendamento!',
                                                           'serializer.data')

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    if request.method == 'GET':
        try:
            appointment = Appointment.objects.get(pk=id)
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data)

        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        try:
            appointment = Appointment.objects.get(pk=id)
            appointment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
