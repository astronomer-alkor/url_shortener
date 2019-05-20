import re
from string import ascii_letters, digits
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Url


class UrlField(forms.CharField):
    def validate(self, value):
        super().validate(value)
        if not re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}'
                        r'\b([-a-zA-Z0-9@:%_\+.~#?&\/=]*)', value):
            raise ValidationError('Неверная ссылка')


class CustomUrlField(forms.CharField):
    def validate(self, value):
        if not value:
            return None
        elif len(value) > 20:
            raise ValidationError('Максимальная длина - 20 символов')
        elif Url.is_short_url_exist(value):
            raise ValidationError('Ссылка уже занята')
        elif not re.match(r'[a-zA-z0-9_\-]+', value):
            raise ValidationError('Неверный формат. Корректные символы: a-z A-z 0-9 _ -')
        return None


class UsernameField(forms.CharField):
    def __init__(self, write=False):
        super().__init__()
        self.write = write

    def validate(self, value):
        super().validate(value)
        if self.write:
            if not set(value).issubset(set(ascii_letters + digits + '-_.')):
                raise ValidationError('Неверный формат. Корректные символы: a-z A-z 0-9 _ - .')
            elif len(value) < 5:
                raise ValidationError('Минимальная длина - 5 символов')
            elif len(value) > 15:
                raise ValidationError('Максимальная длина - 15 символов')
            elif User.objects.filter(username=value):
                raise ValidationError('Логин уже занят')


class EmailField(forms.CharField):
    def __init__(self, write=False):
        super().__init__()
        self.write = write

    def validate(self, value):
        super().validate(value)
        if self.write:
            if not re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', value):
                raise ValidationError('Некорректный E-mail')
            elif User.objects.filter(email=value):
                raise ValidationError('E-mail уже занят')


class PasswordField(forms.CharField):
    # Todo: доделать валидацию пароля
    def validate(self, value):
        super().validate(value)


class ShortUrlForm(forms.Form):
    long_url = UrlField()
    custom_url = CustomUrlField(max_length=20)


class SignUpForm(forms.Form):
    username = UsernameField(write=True)
    email = EmailField(write=True)
    password = PasswordField()
    password2 = PasswordField()

    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            password = cleaned_data['password']
            password2 = cleaned_data['password2']
        except KeyError:
            return None
        if password != password2:
            raise ValidationError("Пароли не совпадают")
        return None


class SignInForm(forms.Form):
    username = UsernameField()
    password = PasswordField()

    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            if not User.objects.filter(username=cleaned_data['username'],
                                       password=cleaned_data['password']):
                raise ValidationError('Неверные логин или пароль')
        except KeyError:
            return None


class RestorationForm(forms.Form):
    email = EmailField()

    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            if not User.objects.filter(email=cleaned_data['email']):
                raise ValidationError('Неверный E-mail')
        except KeyError:
            return None

