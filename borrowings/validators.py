from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone


def date_limit_take_book(value):
    limit = 30
    if value > timezone.now().date() + timedelta(days=limit):
        raise ValidationError(f"The date cannot be more than {limit} days from today.")


def date_limit_return_book(value):
    limit = 60
    if value > timezone.now().date() + timedelta(days=limit):
        raise ValidationError(
            f"It is not possible to return the book after this {limit} days without a large fine"
        )
