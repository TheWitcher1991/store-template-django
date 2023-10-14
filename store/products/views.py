from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from products.models import ProductCategory, Product, Basket
from users.models import User


# Главная страница
def index(request):
    context = {
        'title': 'Store',
        'is_promotion': True
    }
    return render(request, 'products/index.html', context)


# Каталог товаров
def products(request):
    context = {
        'title': 'Store - Каталог',
        'categories': ProductCategory.objects.all(),
        'products': Product.objects.all()
    }
    return render(request, 'products/products.html', context)


# Добавление в корзину
@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# Удаление из корзины
@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
