from django.contrib import admin

from Libary.models import Book, CustomUser, Borrowing, Payment

admin.site.register(Book)
admin.site.register(CustomUser)
admin.site.register(Borrowing)
admin.site.register(Payment)
