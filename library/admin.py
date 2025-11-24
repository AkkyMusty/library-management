from django.contrib import admin

from .models import Book, BookCopy, BorrowRecord


# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn')
    search_fields = ('title', 'author', 'isbn')

@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ('book', 'barcode', 'status')
    list_filter = ('status', 'book')
    search_fields = ('barcode',)

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('copy', 'user', 'borrow_date', 'due_date', 'return_date')
    list_filter = ('borrow_date', 'return_date')
    search_fields = ('user__username', 'copy__barcode')


