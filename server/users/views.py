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
        name = request.POST.get('name')

        try:
            validate_password(password)
        except ValidationError:
            self.result = 'Пароль или email указаны неверно'
            return self.get(request, *args, **kwargs)

        if all((not is_authenticated, email, password)):
            user_qs = User.objects.filter(
                email=email
            )
            if user_qs.count() == 0:
                user = User()
                user.email = email
                user.first_name = name
                user.set_password(password)
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
                return redirect('users:aftercheck')
            else:
                self.result = 'Пользователь с таким email уже существует'
        else:
            self.result = 'Данные указаны неверно'
        return self.get(request, *args, **kwargs)


class LoginView(TemplateView):

    template_name = 'pages/login.html'

    def get(self, request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated
        if is_authenticated:
            return redirect('/')
        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated
        if is_authenticated:
            return redirect('/')

        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        print(email)
        print(password)

        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
        else:
            self.result = 'error'
        return super(LoginView, self).get(request, *args, **kwargs)


class UserAftercheckView(TemplateView):

    template_name = 'pages/aftercheck.html'


class LogoutView(TemplateView):
    template_name = "pages/login.html"

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")