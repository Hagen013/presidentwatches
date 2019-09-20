from config.celery import app

from django.contrib.auth import get_user_model
from django.conf import settings

from core.mail import Mail

User = get_user_model()

if settings.DEBUG:
    BASE_URL = 'http://localhost:8080'
else:
    BASE_URL = 'https//presidentwatches.ru'


@app.task
def generate_verification_mail(pk):
    user = User.objects.get(pk=pk)
    context = {
        'user': user,
        'BASE_URL': BASE_URL
    }
    template = 'mail/verification.html'
    title = 'Подтверждение регистрации'

    mail = Mail(
        title=title,
        template=template,
        recipient=user.email,
        context=context
    )
    mail.send()

@app.task
def send_new_password(pk, password):
    user = User.objects.get(pk=pk)
    context = {
        'user': user,
        'password': password,
        'BASE_URL': BASE_URL
    }
    template = 'mail/password-confirmation.html'

    mail = Mail(
        title='Смена пароля',
        template=template,
        recipient=user.email,
        context=context
    )
    mail.send()