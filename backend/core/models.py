from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """ 
    create User class at the beginning of each project.
    that we can modify it later if necessary
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    USERNAME_FIELD = 'username'
