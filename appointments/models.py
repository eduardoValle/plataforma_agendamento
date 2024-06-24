from django.db import models

from register.models import CustomUser


class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField()
    service = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed')])

    REQUIRED_FIELDS = [user, date, service]

    def __str__(self):
        return f'Serviço: {self.service} | Status: {self.status}'
