from django.shortcuts import render, get_object_or_404
from .models import Book, BookCopy
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

def borrow_copy(request, copy_id):
    copy = get_object_or_404(BookCopy, id=copy_id)

    # Only allow borrowing if available
    if copy.status != BookCopy.STATUS_AVAILABLE:
        return HttpResponseRedirect(
            reverse('book_detail', args=[copy.book.id])
        )

    # Mark the copy as borrowed
    copy.status = BookCopy.STATUS_BORROWED
    copy.save()

    # Create a borrow record
    BorrowRecord.objects.create(
        user=request.user,                     # the logged-in user
        copy=copy,
        borrow_date=timezone.now(),
        due_date=timezone.now() + timezone.timedelta(days=14)  # 2 weeks
    )

    return HttpResponseRedirect(
        reverse('book_detail', args=[copy.book.id])
    )