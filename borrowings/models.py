from django.db import models

from Libary.models import Book
from user.models import User


class Borrowing(models.Model):
    Borrow = models.DateField()
    Expected_return_date = models.DateField()
    Actual_return_date = models.DateField(null=True, blank=True)
    Book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="Borrowing")
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Borrowing")

    def __str__(self):
        return f"{self.User.username} = name: {self.User.first_name}, last name: {self.User.last_name}"
