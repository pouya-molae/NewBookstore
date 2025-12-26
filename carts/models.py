from django.db import models
from catalog.models import Book


class Cart(models.Model):
    # سبد خرید موقت برای کاربرانی که لاگین نیستند
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        # ⬅️ اصلاحیه مهم: تغییر نام جدول به حروف کوچک برای سازگاری بهتر با PostgreSQL
        # این کار خطای "relation 'Cart' does not exist" را رفع می‌کند.
        db_table = 'cart'
        ordering = ['date_added']

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        # ⬅️ اصلاحیه: تغییر نام جدول به حروف کوچک
        db_table = 'cartitem'

    def sub_total(self):
        # محاسبه قیمت کل آیتم
        return self.book.price * self.quantity

    def __str__(self):
        return self.book.titlepy