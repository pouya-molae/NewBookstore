from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Book
from .cart import Cart

def add_cart(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.add(book=book)
    return redirect('carts:cart_detail')

def cart_remove(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    return redirect('carts:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'carts/detail.html', {'cart': cart})