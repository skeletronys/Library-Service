from django.db import models
from user.models import User


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
    daily_fee = models.DecimalField(max_digits=100)


class CustomUser(User):
    pass


class Borrowing(models.Model):
    Borrow = models.DateField()
    Expected_return_date = models.DateField()
    Actual_return_date = models.DateField()
    Book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="Borrowing")
    User = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="Borrowing"
    )
