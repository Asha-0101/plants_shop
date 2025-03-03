from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomerUserForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control border-success', 'placeholder': 'Enter your phone number'}),
        required=True,
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control border-success', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control border-success', 'placeholder': 'Enter your email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control border-success', 'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control border-success', 'placeholder': 'Confirm password'}),
        }