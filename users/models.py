from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    '''
    Custom User Model

    This model extends the default Django `AbstractUser` model and adds additional fields and customizations.
    '''
    
    email = models.EmailField(unique=True)
    friends = models.ManyToManyField("self")

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name ='CustomUser'