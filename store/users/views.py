from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegisterForm
from users.models import EmailVerification, User


# Страница авторизации
class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'


# Страница регистрации
class UserRegisterView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно создали аккаунт'
    title = 'Store - Регистрация'


# Страница профиль
class UserProfileView(UpdateView, LoginRequiredMixin):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['title'] = 'Store - Профиль'
    #    context['baskets'] = Basket.objects.filter(user=self.object)
    #    return context


# Подтверждение электронной почты
class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'Store - Подтверждение электронной почты'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))


# def login(request):
#    if request.method == 'POST':
#        form = UserLoginForm(data=request.POST)
#        if form.is_valid():
#            username = request.POST['username']
#            password = request.POST['password']
#            user = auth.authenticate(username=username, password=password)
#            if user:
#                auth.login(request, user)
#                return HttpResponseRedirect(reverse('index'))
#    else:
#        form = UserLoginForm()
#    context = {
#        'title': 'Store - Авторизация',
#        'form': form
#     }
#    return render(request, 'users/login.html', context)


# def register(request):
#    if request.method == 'POST':
#        form = UserRegisterForm(data=request.POST)
#        if form.is_valid():
#            form.save()
#            messages.success(request, 'Вы успешно создали аккаунт')
#            return HttpResponseRedirect(reverse('users:login'))
#    else:
#        form = UserRegisterForm()
#    context = {
#        'title': 'Store - Регистрация',
#        'form': form
#    }
#    return render(request, 'users/register.html', context)


# @login_required
# def profile(request):
#    if request.method == 'POST':
#        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#        if form.is_valid():
#            form.save()
#            return HttpResponseRedirect(reverse('users:profile'))
#    else:
#        form = UserProfileForm(instance=request.user)
#
#    context = {
#        'title': 'Store - Профиль',
#        'form': form,
#        'baskets': Basket.objects.filter(user=request.user),
#    }
#    return render(request, 'users/profile.html', context)


# Выход из аккаунта
# def logout(request):
#    auth.logout(request)
#    return HttpResponseRedirect(reverse('index'))
