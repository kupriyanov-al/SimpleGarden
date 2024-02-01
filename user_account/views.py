from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from user_account.forms import LoginForm
# Create your views here.


class CastomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'user_account/login.html'
    extra_context = {'title': 'Авторизация'}
    
    def get_success_url(self):
        return reverse_lazy('home')
