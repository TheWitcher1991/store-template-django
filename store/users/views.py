from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import auth, messages

from products.models import Basket
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm


# Страница авторизации
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {
        'title': 'Store - авторизация',
        'form': form
     }
    return render(request, 'users/login.html', context)


# Страница регистрации
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно создали аккаунт')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegisterForm()
    context = {
        'title': 'Store - регистрация',
        'form': form
    }
    return render(request, 'users/register.html', context)


# Страница профиль
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'title': 'Store - профиль',
        'form': form,
        'baskets': Basket.objects.filter(user=request.user),
    }
    return render(request, 'users/profile.html', context)


# Выход из аккаунта
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
