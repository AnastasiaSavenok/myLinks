from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from . import managers


class CustomUser(AbstractUser):

    username = None
    email = models.EmailField(_('email address'), unique=True)
    token = models.PositiveIntegerField(default=00000)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = managers.CustomUserManager()

    def __str__(self):
        return self.email
