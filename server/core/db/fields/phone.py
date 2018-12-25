from django.db import models
from django.core.validators import RegexValidator


class PhoneNumberField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs["verbose_name"] = "phone number"
        kwargs["max_length"] = 17
        kwargs["validators"] = [
                RegexValidator(
                    regex=r'^\+?1?\d{9,15}$',
                    message='Invalid phone number',
                )
            ]
        super(PhoneNumberField, self).__init__(*args, **kwargs)
