from django.db import models
from django.contrib.auth.models import AbstractUser


class Book(models.Model):
    class CoverType(models.TextChoices):
        HARD = "Hard", "Hard Cover"
        SOFT = "Soft", "Soft Cover"

    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=4,
        choices=CoverType.choices,
    )
    inventory = models.IntegerField()
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Customer(AbstractUser):
    pass

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
