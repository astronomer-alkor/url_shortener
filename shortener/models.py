from hashlib import sha256
from django.db import models
from django.contrib.auth.models import User


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


def encrypt_password(password):
    return sha256(password.encode()).hexdigest()


def sign_up(data):
    password = encrypt_password(data['password'])
    user = User.objects.create(username=data['username'],
                               email=data['email'],
                               password=password)
    user.save()
    return user


def get_user(data):
    password = encrypt_password(data['password'])
    user = User.objects.filter(username=data['username'],
                               password=password)
    if user:
        return user[0]
    return None
