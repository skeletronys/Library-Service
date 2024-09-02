from celery import shared_task
from django.utils import timezone
from borrowings.models import Borrowing
from telegramBot import send_telegram_message


@shared_task
def check_overdue_borrowings():
    now = timezone.now().date()
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=now, actual_return_date__isnull=True
    )

    if overdue_borrowings.exists():
        print(f"Found {overdue_borrowings.count()} overdue borrowings.")
        for borrowing in overdue_borrowings:
            message = (
                f"This day: {now.strftime('%A, %B %d, %Y')}\n"
                f"Borrowing overdue!\n"
                f"Borrowing id: {borrowing.id}\n"
                f"Book: {borrowing.book.name}\n"
                f"User: {borrowing.user.first_name} {borrowing.user.last_name}\n"
                f"Borrow date: {borrowing.borrow}\n"
                f"Expected return date: {borrowing.expected_return_date}"
            )
            send_telegram_message(message)
    else:
        print("No borrowings overdue today.")
        send_telegram_message("No borrowings overdue today!")


# celery -A Library_Service worker -l info -P gevent
# celery -A Library_Service beat -l info
