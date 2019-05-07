from django.shortcuts import render
from .forms import ShortUrlForm
from .url_utils import generate_short_url


def index(request):
    if request.method == 'POST':
        form = ShortUrlForm(request.POST)
        short_url = ''
        if form.is_valid():
            short_url = generate_short_url(request.POST['long_url'], request.POST['custom_url'])
        return render(request, 'shortener/index.html', {'form': form, 'short_url': short_url})
    return render(request, 'shortener/index.html')
