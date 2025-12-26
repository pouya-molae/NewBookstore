from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # مسیر /catalog/ (نمایش لیست تمام کتاب‌ها)
    path('', views.book_list, name='book_list'),

    # مسیر /catalog/category_slug/ (نمایش کتاب‌های یک دسته‌بندی خاص)
    path('<slug:category_slug>/',
         views.book_list,
         name='book_list_by_category'),

    # مسیر /catalog/id/slug/ (نمایش جزئیات یک کتاب)
    path('<int:id>/<slug:slug>/',
         views.book_detail,
         name='book_detail'),

    path('api/ai-chat/', views.ai_assistant_chat, name='ai_chat'),

    path('category/<slug:category_slug>/', views.book_list, name='book_list_by_category'),
]