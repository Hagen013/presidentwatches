from django.template.loader import render_to_string
from django.core.mail import EmailMessage

EMAIL_REPLY_TO = "info@presidentwatches.ru"


class Mail():

    def __init__(self, title, template, recipient, context={}):
        self.title = title
        self.template = template
        self.recipient = recipient
        self.context = context

    def render(self):
        return render_to_string(self.template, {"title": self.title, **self.context})

    def send(self):
        title = self.title
        html_message = self.render()
        email = EmailMessage(
            self.title,
            html_message,
            to=[self.recipient],
            reply_to=[EMAIL_REPLY_TO],
        )

        email.content_subtype = "html"
        email.send()