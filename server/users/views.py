from random import randint

from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import Http404

from tasks.users import generate_verification_mail

from cart.cart import Cart
from shop.models import CategoryPage as Node
from shop.models import ProductPage as Product
from core.utils import custom_redirect_v2
from .models import UserTemporaryMailingAccessToken as Token

# удалить
from cart.models import Promocode, GiftSalesTable

User = get_user_model()


class ProfileView(TemplateView):
    """
    View для просмотра личной страницы пользователя
    """
    template_name = 'pages/profile.html'

    def get(self, request, *args, **kwargs):
        querydict = request.GET.dict()
        if not request.user.is_authenticated:

            user_login = querydict.get('login', None)
            password = querydict.get('password', None)
            redirect_to = querydict.get('redirect', None)

            if user_login is not None and password is not None:
                user = authenticate(request, username=user_login, password=password)
                if not user:
                    return custom_redirect_v2(
                        'users:login',
                        **querydict
                    )
                else:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    self.cart = Cart(request)
                    self.cart.login_sync()
                    querydict.pop('login')
                    querydict.pop('password')
                    return custom_redirect_v2(
                        'users:profile',
                        **querydict
                    )

            return custom_redirect_v2(
                'users:login',
                **querydict
            )
        return super(ProfileView, self).get(request, *args, *kwargs)

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

        try:
            validate_password(password)
        except ValidationError:
            print('Неверный пароль')
            self.result = 'Пароль должен состоять минимум из 8 знаков'
            return self.get(request, *args, **kwargs)


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
                user.is_active = False
                
                try:
                    user.full_clean()
                except ValidationError:
                    self.result = 'Пароль или email указаны неверно'
                    return self.get(request, *args, **kwargs)

                user.set_password(password)
                user.save()
                generate_verification_mail.delay(user.id)
                #login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                self.result = 'Вы успешно зарегестрировались'
                return redirect('users:aftercheck', uuid=user.public_uuid)
            else:
                self.result = 'Пользователь с таким email уже существует'
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
        self.result = None
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

        user = authenticate(request, username=email, password=password)


        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            self.cart = Cart(request)
            self.cart.login_sync()
            return redirect('/')
        else:
            self.result = 'Пароль или логин указаны неверно'
        return super(LoginView, self).get(request, *args, **kwargs)

    def get_context_data(self, *arsg, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['result'] = self.result
        return context


class UserAftercheckView(TemplateView):

    template_name = 'pages/user-verification.html'

    def get_user(self, public_uuid):
        try:
            return User.objects.get(public_uuid=public_uuid)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, uuid, *args, **kwargs):
        self.user = self.get_user(uuid)
        return super(UserAftercheckView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(UserAftercheckView, self).get_context_data(*args, **kwargs)
        context['user'] = self.user
        return context


class LogoutView(TemplateView):
    template_name = "pages/login.html"

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")


class UserEmailVerificationView(TemplateView):

    """
    View, принимающая uuid переданный в письме пользователю,
    завершающая регистрацию через Email
    """

    template_name = 'pages/email-confirmation.html'

    def get_user(self, uuid):
        try:
            return User.objects.get(
                uuid=uuid
            )
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, uuid, *args, **kwargs):
        user = self.get_user(uuid)
        user.is_active = True
        user.verified = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        self.cart = Cart(request)
        self.cart.login_sync()
        return super(UserEmailVerificationView, self).get(request, *args, **kwargs)
        

class UserPasswordConfirmationView(TemplateView):

    def get_user(self, uuid):
        try:
            return User.objects.get(
                uuid=uuid
            )
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, uuid, *args, **kwargs):
        password = request.GET.get('password', None)
        if password is None:
            raise Http404
        user = self.get_user(uuid)
        user.verified = True
        user.set_password(password)
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        self.cart = Cart(request)
        self.cart.login_sync()
        return redirect('/u/profile/')


class UserUUIDMixin():

    def get_user(self, uuid):
        try:
            return User.objects.get(
                uuid=uuid
            )
        except ObjectDoesNotExist:
            raise Http404


class UserClubPriceExistingView(TemplateView, UserUUIDMixin):

    def get(self, request, uuid, *args, **kwargs):
        slug = request.GET.get('slug')
        user = self.get_user(uuid)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        self.cart = Cart(request)
        self.cart.login_sync()
        url = '/watches/{slug}/'.format(slug=slug)
        return redirect(url)


class UserClubPriceCreatedView(TemplateView, UserUUIDMixin):

    def get(self, request, uuid, *args, **kwargs):
        slug = request.GET.get('slug')
        user = self.get_user(uuid)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        self.cart = Cart(request)
        self.cart.login_sync()
        url = '/watches/{slug}/'.format(slug=slug)
        return redirect(url)


class UserMailingView(TemplateView):

    template_name = 'pages/mailing.html'

    def get_user(self, uuid):
        try:
            return User.objects.get(
                uuid=uuid
            )
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, uuid, *args, **kwargs):
        user = self.get_user(uuid)
        user.verified = True
        user.save()
        self.user = user
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        self.cart = Cart(request)
        self.cart.login_sync()
        return super(UserMailingView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(UserMailingView, self).get_context_data(*args, **kwargs)
        context['user'] = self.user
        return context


class UserTestView(TemplateView):

    template_name = 'mail/gift-price.html'

    def get_context_data(self, *args, **kwargs):
        context = super(UserTestView, self).get_context_data(*args, **kwargs)
        product = Product.objects.get(model='SSB301P1')
        email = 'vlad.sivh@gmail.com'
        user = User.objects.get(email=email)
        password = None
        promocode = Promocode.objects.filter(datatype=5)[0]
        table = GiftSalesTable.objects.first()
        sales = table.sales
        multiplier = sales.get(product.brand)
        percentage = int(multiplier * 100)
        sale_amount = product._price * multiplier

        context = {
            'BASE_URL': 'http://localhost:8000',
            'email': email,
            'user': user,
            'password': password,
            'promocode': promocode,
            'product': product,
            'percentage': percentage,
            'sale_amount': sale_amount
        }

        return context


class UserMailingRedirectView(TemplateView):

    template_name = 'pages/mailing.html'

    def get_user(self, uuid):
        try:
            return User.objects.get(
                uuid=uuid
            )
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, uuid, *args, **kwargs):
        user = self.get_user(uuid)
        user.is_active = True
        user.verified = True
        user.save()
        self.user = user
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        self.cart = Cart(request)
        self.cart.login_sync()
        category_id = request.GET.get('category', None)
        email = user.email

        node = None
        if category_id is not None:
            try:
                node = Node.objects.get(
                    id=category_id
                )
            except ObjectDoesNotExist:
                node = Node.objects.get(
                    slug=''
                )
        else:
            node = Node.objects.get(
                slug=''
            )


        url = '/shop/watches/{slug}?rr_email={email}'.format(
            slug=node.slug,
            email=email
        )

        return redirect(url)


class GiftPriceRedirectView(TemplateView):

    template_name = 'pages/mailing.html'

    def get_user(self, uuid):
        try:
            return User.objects.get(
                uuid=uuid
            )
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, uuid, *args, **kwargs):
        user = self.get_user(uuid=uuid)
        product_pk = request.GET.get('product', None)
        promocode_name = request.GET.get('promocode', None)
        if product_pk is None or promocode_name is None:
            raise Http404
        
        try:
            product = Product.objects.get(id=product_pk)
            promocode = Promocode.objects.get(name=promocode_name)
        except ObjectDoesNotExist:
            raise Http404

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        self.cart = Cart(request)
        self.cart.login_sync()
        self.cart.apply_promocode(promocode)
        try:
            sale = product.price * promocode.sales.get(product.brand)
            url = '/watches/{slug}/?promo_sale={sale}'.format(
                slug=product.slug,
                sale=sale
            )
        except:
            url = '/watches/{slug}/'.format(
                slug=product.slug,
            )

        return redirect(url)


class MailingTokenView(TemplateView):

    model = Token

    def get(self, request, uuid, *args, **kwargs):
        category = request.get('category')
        email = request.get('email')
        try:
            token = self.model.objects.get(
                token=uuid
            )
            node = CategoryPage.objects.get(pk=category)
        except ObjectDoesNotExist:
            raise Http404

        user = token.user
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        self.cart = Cart(request)
        self.cart.login_sync()
        self.cart.apply_promocode(promocode)
        user.verified = True
        user.save()

        url = '/shop/watches/{slug}?rr_email={email}'.format(
            slug=node.slug,
            email=email
        )

        return redirect(url)
