from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    isbn = models.CharField(max_length=13, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} — {self.author}"

class BookCopy(models.Model):
    STATUS_AVAILABLE = 'available'
    STATUS_BORROWED = 'borrowed'
    STATUS_RESERVED = 'reserved'

    STATUS_CHOICES = [
        (STATUS_AVAILABLE, 'Available'),
        (STATUS_BORROWED, 'Borrowed'),
        (STATUS_RESERVED, 'Reserved'),
    ]

    book = models.ForeignKey(Book, related_name='copies', on_delete=models.CASCADE)
    barcode = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE)

    def __str__(self):
        return f"{self.book.title} — copy {self.barcode} ({self.status})"


class BorrowRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='borrow_records', on_delete=models.CASCADE)
    copy = models.ForeignKey(BookCopy, related_name='borrow_records', on_delete=models.PROTECT)
    borrow_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()  # set when borrowing
    return_date = models.DateTimeField(null=True, blank=True)

    def is_overdue(self):
        return self.return_date is None and timezone.now() > self.due_date

    def __str__(self):
        return f"{self.copy} borrowed by {self.user}"
