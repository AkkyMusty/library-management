from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.urls import reverse
from django.utils import timezone
from .forms import BookForm
from .models import Book, BookCopy, BorrowRecord


# Create your views here.


def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    copies = book.copies.all()  # because we used related_name='copies'

    available_count = book.copies.filter(status='available').count()
    borrowed_count = book.copies.filter(status='borrowed').count()
    reserved_count = book.copies.filter(status='reserved').count()

    return render(request, 'library/book_detail.html', {
        'book': book,
        'copies': copies,
        'available_count': available_count,
        'borrowed_count': borrowed_count,
        'reserved_count': reserved_count,
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

def return_copy(request, copy_id):
    copy = get_object_or_404(BookCopy, id=copy_id)

    # Only borrowed copies can be returned
    if copy.status != BookCopy.STATUS_BORROWED:
        return HttpResponseRedirect(
            reverse('book_detail', args=[copy.book.id])
        )

    # Find the active borrow record (the one without a return date)
    record = BorrowRecord.objects.filter(copy=copy, return_date__isnull=True).first()

    if record:
        record.return_date = timezone.now()
        record.save()

    # Change copy status back to available
    copy.status = BookCopy.STATUS_AVAILABLE
    copy.save()

    return HttpResponseRedirect(
        reverse('book_detail', args=[copy.book.id])
    )



def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return redirect('book_detail', book.id)
    else:
        form = BookForm()

    return render(request, 'library/add_book.html', {'form': form})


def available_books(request):
    books = Book.objects.annotate(
        available_count=Count('copies', filter=Q(copies__status='available'))
    ).filter(available_count__gt=0)

    return render(request, 'library/available_books.html', {'books': books})
