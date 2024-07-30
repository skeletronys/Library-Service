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
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)


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


class Payment(models.Model):

    class StatusType(models.TextChoices):
        PENDING = "Pending", "Pending"
        PAID = "Paid", "Paid"

    class Types(models.TextChoices):
        PAYMENT = "Payment", "Payment"
        FINE = "Fine", "Fine"

    status = models.CharField(
        max_length=7,
        choices=StatusType.choices,
    )
    type = models.CharField(
        max_length=7,
        choices=Types.choices,
    )
    borrowing = models.ForeignKey(
        Borrowing, on_delete=models.CASCADE, related_name="payments"
    )
    session_url = models.URLField(
        max_length=200, blank=True, null=True, help_text="URL to stripe payment session"
    )
    session_id = models.CharField(
        max_length=255, blank=True, null=True, help_text="ID of stripe payment session"
    )
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)
