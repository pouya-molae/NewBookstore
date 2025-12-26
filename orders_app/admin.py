from django.contrib import admin
from .models import Order, OrderItem

from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['book']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # ستون‌هایی که در لیست سفارشات دیده می‌شوند
    list_display = ['id', 'first_name', 'last_name', 'email', 'paid', 'created', 'updated']
    # فیلتر کردن بر اساس وضعیت پرداخت و زمان
    list_filter = ['paid', 'created', 'updated']
    # اضافه کردن آیتم‌های سفارش به صورت خطی در صفحه جزئیات سفارش
    inlines = [OrderItemInline]
    # قابلیت جستجو
    search_fields = ['first_name', 'last_name', 'email']