from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('borrow/<int:copy_id>/', views.borrow_copy, name='borrow_copy'),
    path('return/<int:copy_id>/', views.return_copy, name='return_copy'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/available/', views.available_books, name='available_books'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),





]
