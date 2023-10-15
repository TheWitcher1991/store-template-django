from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import ListView, TemplateView

from products.models import Basket, Product, ProductCategory


# Главная страница
class IndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store'
        context['is_promotion'] = True
        return context


# Каталог товаров
class ProductsListView(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3

    def get_queryset(self):
        objects = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return objects.filter(category_id=category_id) if category_id else objects
        # return Product.objects.filter(category_id=self.kwargs.get('category_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store - Каталог'
        context['categories'] = ProductCategory.objects.all()
        return context


# Добавить в корзину
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
