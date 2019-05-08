from django.shortcuts import render, redirect
from django.http import Http404
from .forms import ShortUrlForm
from .url_utils import generate_short_url
from .models import Url


def index(request):
    if request.method == 'POST':
        form = ShortUrlForm(request.POST)
        short_url = ''
        if form.is_valid():
            short_url = '/'.join((request.get_host(),
                                  generate_short_url(request.POST['long_url'], request.POST['custom_url'])))
        return render(request, 'shortener/index.html', {'form': form,
                                                        'short_url': short_url})
    return render(request, 'shortener/index.html')


def redirect_short_url(request, url):
    url_object = Url.get_url_object(url)
    if url_object:
        return redirect(url_object.long_url)
    raise Http404()
