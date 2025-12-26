from django.contrib import admin
from .models import Cart, CartItem

# ثبت مدل Cart
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    # استفاده از فیلدهای موجود در مدل Cart
    list_display = ('cart_id', 'date_added',)
    list_filter = ('date_added',)

# ثبت مدل CartItem
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    # نمایش کتاب، سبد خرید، تعداد و زیرمجموعه قیمت
    list_display = ('book', 'cart', 'quantity', 'active', 'sub_total')
    # یک متد برای نمایش قیمت کلی آیتم (باید در مدل CartItem تعریف شود)
    readonly_fields = ('sub_total',)

    # ⬅️ نکته: مطمئن شوید متد sub_total در models.py وجود دارد.
