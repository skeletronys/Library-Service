from django.db import models

from borrowings.validators import date_limit_take_book, date_limit_return_book
from user.models import User


class Borrowing(models.Model):
    Borrow = models.DateField(validators=[date_limit_take_book])
    Expected_return_date = models.DateField(validators=[date_limit_take_book])
    Actual_return_date = models.DateField(
        null=True, blank=True, validators=[date_limit_return_book]
    )
    Book = models.ForeignKey(
        "Libary.Book", on_delete=models.CASCADE, related_name="Borrowing"
    )
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Borrowing")

    def __str__(self):
        return f"{self.User.first_name} {self.User.last_name}"
