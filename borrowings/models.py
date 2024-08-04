from django.db import models

from borrowings.validators import date_limit_take_book, date_limit_return_book
from user.models import User


class Borrowing(models.Model):
    borrow = models.DateField(validators=[date_limit_take_book])
    expected_return_date = models.DateField(validators=[date_limit_take_book])
    actual_return_date = models.DateField(
        null=True, blank=True, validators=[date_limit_return_book]
    )
    book = models.ForeignKey(
        "Libary.Book", on_delete=models.CASCADE, related_name="Borrowing"
    )
    bser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Borrowing")

    def __str__(self):
        return f"{self.User.first_name} {self.User.last_name}"
