import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Order, OrderItem
from .forms import OrderCreateForm
from carts.cart import Cart


@login_required
def order_create(request):
    """
    نمایش فرم سفارش و ثبت نهایی اقلام سبد خرید در دیتابیس.
    استفاده از @login_required برای اجبار کاربر به ورود پیش از خرید.
    """
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # ایجاد شیء سفارش بدون ذخیره نهایی برای افزودن کاربر
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # ثبت تک‌تک کتاب‌های موجود در سبد خرید برای این سفارش
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    book=item['book'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # خالی کردن سبد خرید پس از ثبت موفق
            cart.clear()

            # هدایت کاربر به صفحه پرداخت با شماره سفارش
            return redirect('orders:payment_process', order_id=order.id)
    else:
        # نمایش فرم خالی به همراه اطلاعات پیش‌فرض کاربر (در صورت تمایل)
        form = OrderCreateForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    return render(request, 'orders/order/create.html', {
        'cart': cart,
        'form': form
    })


def payment_process(request, order_id):
    """
    مدیریت درگاه پرداخت فرضی و تایید نهایی سفارش.
    """
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # در اینجا می‌توانید اعتبارسنجی کارت را انجام دهید
        # شبیه‌سازی موفقیت پرداخت
        order.paid = True
        order.save()
        return render(request, 'orders/order/payment_success.html', {'order': order})

    # نمایش صفحه درگاه برای دریافت اطلاعات کارت (شماره ۱۶ رقمی و غیره)
    context = {
        'order': order,
        'total_price': order.get_total_cost()
    }
    return render(request, 'orders/order/payment_gateway.html', context)


@csrf_exempt
def ai_assistant_chat(request):
    """
    بخش چت‌بات هوشمند (قبلاً نوشته شده).
    نکته: برای کارکرد صحیح نیاز به فعال بودن ابزار تغییر آی‌پی روی سرور است.
    """
    if request.method == "POST":
        try:
            import google.generativeai as genai
            data = json.loads(request.body)
            user_msg = data.get('message')

            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(user_msg)

            return JsonResponse({'reply': response.text})
        except Exception as e:
            print(f"AI Error: {str(e)}")
            return JsonResponse({'reply': 'خطا در برقراری ارتباط با هوش مصنوعی. لطفاً اینترنت خود را چک کنید.'},
                                status=500)
    return JsonResponse({'reply': 'درخواست نامعتبر'}, status=400)