from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Admin"
        MENTOR = "mentor", "Mentor"
        LEARNER = "learner", "Learner"

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.LEARNER)
