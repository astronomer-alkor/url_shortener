from hashlib import sha256
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from .mail_sender import send_account_activation, send_password_restoration


class Url(models.Model):
    process_id = models.IntegerField(null=True)
    long_url = models.URLField()
    short_url = models.CharField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    @staticmethod
    def is_short_url_exist(short_url):
        return Url.objects.filter(short_url=short_url)

    @staticmethod
    def get_url_object(short_url, author=None):
        if author:
            url = Url.objects.filter(short_url=short_url, author=author)
        else:
            url = Url.objects.filter(short_url=short_url)
        if url:
            return url[0]
        return None


class UrlManagement(models.Model):
    url = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def create_url(user):
        unique_string = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S.%f') + user.email
        url = sha256(unique_string.encode()).hexdigest()
        url = UrlManagement.objects.create(url=url, user=user)
        url.save()
        return url

    @staticmethod
    def get_url_by_user(user):
        url_object = UrlManagement.objects.filter(user=user)
        if url_object:
            return url_object[0]

    @staticmethod
    def get_url(url):
        url_object = UrlManagement.objects.filter(url=url)
        if url_object:
            return url_object[0]

    @staticmethod
    def delete_url(user):
        UrlManagement.objects.filter(user=user).delete()


def create_url(request, user, url_type, remove_old=False):
    if remove_old:
        UrlManagement.delete_url(user)
    url = UrlManagement.create_url(user)
    return '/'.join((request.get_host(), url_type, f'?key={url.url}'))


def sign_up(data, request):
    user = User.objects.create(username=data['username'],
                               email=data['email'],
                               password=data['password'])
    user.is_active = False
    url = create_url(request, user, url_type='activation')
    send_account_activation(email=data['email'], username=data['username'], url=url)
    user.save()
    return user


def get_user(data):
    user = User.objects.filter(username=data['username'],
                               password=data['password'])
    if user:
        return user[0]
    return None


def restore_password(request, email):
    user = User.objects.filter(email=email)[0]
    url = create_url(request, user, url_type='restore', remove_old=True)
    send_password_restoration(email, user.username, url)
