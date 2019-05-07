import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Url


class UrlField(forms.CharField):
    def validate(self, value):
        if not value:
            raise ValidationError('Поле обязательно для заполнения')
        elif not re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}'
                          r'\b([-a-zA-Z0-9@:%_\+.~#?&\/=]*)', value):
            raise ValidationError('Неверная ссылка')


class CustomUrlField(forms.CharField):
    def validate(self, value):
        if not value:
            return
        if len(value) > 20:
            raise ValidationError('Максимальная длина - 20 символов')
        elif Url.is_short_url_exist(value):
            raise ValidationError('Ссылка уже занята')
        elif not re.match(r'[a-zA-z0-9_\-]+', value):
            raise ValidationError('Неверный формат. Корректные символы: a-z A-z 0-9 _ -')


class ShortUrlForm(forms.Form):
    long_url = UrlField()
    custom_url = CustomUrlField(max_length=20)
