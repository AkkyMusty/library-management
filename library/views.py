from django.shortcuts import render, get_object_or_404
from .models import Book
# Create your views here.


def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    copies = book.copies.all()  # because we used related_name='copies'

    return render(request, 'library/book_detail.html', {
        'book': book,
        'copies': copies
    })