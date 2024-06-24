from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [email, full_name]

    objects = CustomUserManager()

    def __str__(self):
        return f'id: {self.id} | E-mail: {self.email} | Nome: {self.full_name}'
