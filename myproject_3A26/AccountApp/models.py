from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    pass
class Doctor(User):
    pass
class Patient(User):
    pass
            