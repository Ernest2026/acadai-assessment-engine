from django.contrib.auth.models import AbstractUser
from django.db import models

class AcadUser(AbstractUser):
    is_student = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)