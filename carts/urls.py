from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:book_id>/', views.add_cart, name='add_cart'),
    path('remove/<int:book_id>/', views.cart_remove, name='cart_remove'),
]