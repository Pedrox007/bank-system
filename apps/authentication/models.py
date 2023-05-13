from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin

from apps.resources.base_model import BaseModel, CustomUserManager

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    class Meta():
        app_label = 'authentication'