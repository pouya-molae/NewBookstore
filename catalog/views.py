import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Book, Category

# پیکربندی هوش مصنوعی
try:
    import google.generativeai as genai

    # نکته امنیتی: در پروژه واقعی API Key را در فایل .env قرار دهید
    genai.configure(api_key="AIzaSyBjn2uu4D1CDxQRjF5OztW5_f64O6QOTtk")
except ImportError:
    genai = None


# --- نمایش لیست کتاب‌ها با ظاهر جدید ---
def book_list(request):
    categories = Category.objects.all()
    books = Book.objects.filter(available=True)

    # ۱. منطق جستجو (Search)
    query = request.GET.get('q')
    if query:
        books = books.filter(title__icontains=query) | books.filter(author__icontains=query)

    # ۲. فیلتر دسته‌بندی (Category)
    category_id = request.GET.get('category')
    current_category = None
    if category_id:
        current_category = get_object_or_404(Category, id=category_id)
        books = books.filter(category=current_category)

    # ارسال به قالب جدیدی که در مرحله قبل طراحی کردیم
    return render(request, 'catalog/book/list.html', {
        'books': books,
        'categories': categories,
        'current_category': current_category,
        'query': query
    })


# --- جزئیات کتاب ---
def book_detail(request, id):
    book = get_object_or_404(Book, id=id, available=True)
    return render(request, 'catalog/book_detail.html', {'book': book})


# --- چت‌بات هوشمند (AI Assistant) ---
@csrf_exempt
def ai_assistant_chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_msg = data.get('message')

            if not genai:
                return JsonResponse({'reply': 'کتابخانه هوش مصنوعی نصب نیست.'})

            # استخراج موجودی برای راهنمایی دقیق
            all_books = Book.objects.filter(available=True)[:10]
            inventory = "\n".join([f"- {b.title} ({b.price} تومان)" for b in all_books])

            # استفاده از مدل Gemini 1.5 Flash (سریع‌تر و ارزان‌تر برای چت‌بات)
            model = genai.GenerativeModel('gemini-1.5-flash')

            prompt = f"""
            شما "دستیار هوشمند کتابفروشی" هستید. 
            لیست کتاب‌های موجود ما:
            {inventory}

            وظایف:
            1. فقط بر اساس لیست بالا پیشنهاد بده.
            2. صمیمی و بسیار کوتاه (حداکثر ۲ جمله) پاسخ بده.
            3. اگر کتابی را نداریم، بگو "متاسفانه فعلاً نداریم" و یک مورد مشابه از لیست پیشنهاد بده.

            پیام کاربر: {user_msg}
            """

            response = model.generate_content(prompt)
            return JsonResponse({'reply': response.text})

        except Exception as e:
            return JsonResponse({'reply': "خطایی در هوش مصنوعی رخ داد."}, status=500)

    return JsonResponse({'reply': 'درخواست نامعتبر'}, status=400)