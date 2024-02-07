from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


# переопределяем стандартную форму AuthenticationForm
class LoginForm(AuthenticationForm):  
    username = forms.CharField(
        max_length=150,
        label="Login",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'пользователь'
        })
    )
    
    password = forms.CharField(
        max_length=150,
        label="Password",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'пароль',
            'type': 'password',
        })
    )

    class Meta:
        model = User
        fields = ['user', 'password']