from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'تکرار رمز عبور'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'نام کاربری'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ایمیل'}),
        }

    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError('رمز عبور مطابقت ندارد.')
        return cd['confirm_password']