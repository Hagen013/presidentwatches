from django.core.validators import RegexValidator

slug_validator = RegexValidator(
    regex=r'^(($)|(([0-9A-Za-z_.-])+$))',
    message='invalid slug',
)
