from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ 
    create User class at the beginning of each project.
    that we can modify it later if necessary
    """
    email = models.EmailField(unique=True)
