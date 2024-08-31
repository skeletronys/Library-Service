from django.core.validators import URLValidator
from django.db import models

from borrowings.validators import date_limit_take_book, date_limit_return_book
from user.models import User


class OptionalSchemeURLValidator(URLValidator):
    def __call__(self, value):
        if "://" not in value:
            # Validate as if it were http://
            value = "http://" + value
        super(OptionalSchemeURLValidator, self).__call__(value)


class Borrowing(models.Model):
    borrow = models.DateField(validators=[date_limit_take_book])
    expected_return_date = models.DateField(validators=[date_limit_take_book])
    actual_return_date = models.DateField(
        null=True, blank=True, validators=[date_limit_return_book]
    )
    book = models.ForeignKey(
        "Libary.Book", on_delete=models.CASCADE, related_name="Borrowing"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Borrowing")

    def __str__(self):
        return f"ID: {self.id} | Book: {self.book.name} | User: {self.user.first_name} {self.user.last_name}"


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
    session_url = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="URL to stripe payment session",
        validators=[OptionalSchemeURLValidator],
    )
    session_id = models.CharField(
        max_length=255, blank=True, null=True, help_text="ID of stripe payment session"
    )
    money_to_pay = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return f"{self.status} {self.type}"
