from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from shared.fields import EmailLowerCaseField


class User(AbstractBaseUser, PermissionsMixin):
    email = EmailLowerCaseField(unique=True)

    # Internals
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
