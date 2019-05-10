from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import login, logout
from .forms import ShortUrlForm, SignUpForm, SignInForm
from .url_utils import generate_short_url
from .models import Url, sign_up, get_user


def index(request):
    if request.method == 'POST':
        if 'generate_url' in request.POST:
            form = ShortUrlForm(request.POST)
            short_url = ''
            if form.is_valid():
                short_url = '/'.join((request.get_host(),
                                      generate_short_url(request.POST['long_url'], request.POST['custom_url'])))
            return render(request, 'shortener/index.html', {'form': form,
                                                            'short_url': short_url,
                                                            'user': request.user})
        elif 'sign_up' in request.POST:
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = sign_up(form.cleaned_data)
                login(request, user)
                form = None
            return render(request, 'shortener/index.html', {'sign_up_form': form,
                                                            'user': request.user})
        elif 'sign_in' in request.POST:
            form = SignInForm(request.POST)
            if form.is_valid():
                user = get_user(form.cleaned_data)
                login(request, user)
                form = None
            return render(request, 'shortener/index.html', {'sign_in_form': form,
                                                            'user': request.user})
        elif 'logout' in request.POST:
            logout(request)
    return render(request, 'shortener/index.html', {'user': request.user})


def redirect_short_url(request, url):
    url_object = Url.get_url_object(url)
    if url_object:
        return redirect(url_object.long_url)
    raise Http404()
