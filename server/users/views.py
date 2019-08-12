from random import randint

from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

User = get_user_model()


class ProfileView(TemplateView):
    """
    View для просмотра личной страницы пользователя
    """
    template_name = 'pages/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        return context


class RegisterView(TemplateView):

    template_name = 'pages/register.html'
    result = None

    def get(self, request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated
        if is_authenticated:
            return redirect('/')
        else:
            return super(RegisterView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        is_authenticated = request.user.is_authenticated
        if is_authenticated:
            return redirect("/")

        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name', '')

        print(email)
        print(password)
        print(name)

        print('tsoy')
        print('hoy')

        try:
            validate_password(password)
        except ValidationError:
            print('Неверный пароль')
            self.result = 'Пароль должен состоять минимум из 8 знаков'
            return self.get(request, *args, **kwargs)

        print('Пароль верен')

        if all((not is_authenticated, email, password)):
            user_qs = User.objects.filter(
                email=email
            )
            if user_qs.count() == 0:
                user = User()
                user.email = email
                user.first_name = name
                user.password = password
                user.username = email
                user.is_active = True
                
                try:
                    user.full_clean()
                except ValidationError:
                    self.result = 'Пароль или email указаны неверно'
                    return self.get(request, *args, **kwargs)

                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                self.result = 'Вы успешно зарегестрировались'
                return redirect('/')
                print('Вы успешно зарегестрировались')
            else:
                self.result = 'Пользователь с таким email уже существует'
                print('Пользователь с таким email уже существует')
        else:
            print('Данные указаны неверно')
            self.result = 'Данные указаны неверно'
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, *arsg, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['result'] = self.result
        return context



class LoginView(TemplateView):

    template_name = 'pages/login.html'

    def get(self, request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated
        if is_authenticated:
            return redirect('/')
        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.result = None

        is_authenticated = request.user.is_authenticated
        if is_authenticated:
            return redirect('/')

        email = request.POST.get('email')
        password = request.POST.get('password')
        last_user = User.objects.last()
        print(last_user.check_password(password))

        user = authenticate(request, username=email, password=password)

        print(email)
        print(password)

        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
        else:
            self.result = 'Пароль или логин указаны неверно'
        return super(LoginView, self).get(request, *args, **kwargs)

    def get_context_data(self, *arsg, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['result'] = self.result
        return context


class UserAftercheckView(TemplateView):

    template_name = 'pages/aftercheck.html'


class LogoutView(TemplateView):
    template_name = "pages/login.html"

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")


class UserEmailVerificationView(TemplateView):
    pass
