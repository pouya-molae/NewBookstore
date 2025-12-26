from django.contrib import admin
from django.urls import path, include
# ایمپورت‌های لازم برای مدیریت فایل‌های رسانه‌ای (تصاویر)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # مسیر پیش‌فرض پنل مدیریت
    path('admin/', admin.site.urls),

    # ⬅️ مسیرهای اپلیکیشن احراز هویت (Login, Register)
    path('accounts/', include('accounts.urls', namespace='accounts')),

    # ⬅️ مسیرهای اپلیکیشن سبد خرید
    path('cart/', include('carts.urls', namespace='carts')),

    # ⬅️ مسیرهای اپلیکیشن کاتالوگ (صفحه اصلی پروژه)
    path('', include('catalog.urls', namespace='catalog')),

    path('orders/', include('orders_app.urls', namespace='orders')),
]

# ⬅️ مدیریت فایل‌های رسانه‌ای (تصاویر آپلود شده) در حالت Debug
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)