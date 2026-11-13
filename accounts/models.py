from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        CASHIER = "CASHIER", "Cashier"
        OWNER = "OWNER", "Owner"

    role = models.CharField(
        max_length=10, choices=Role.choices,
        default=Role.CASHIER)
    contact_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username