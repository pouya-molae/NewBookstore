from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-xl', 'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-xl', 'placeholder': 'نام خانوادگی'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-3 border rounded-xl', 'placeholder': 'ایمیل'}),
            'address': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-xl', 'placeholder': 'آدرس دقیق'}),
            'postal_code': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-xl', 'placeholder': 'کد پستی'}),
            'city': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-xl', 'placeholder': 'شهر'}),
        } # مطمئن شوید این علامت در انتها درست بسته شده است