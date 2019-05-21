from django.shortcuts import (
    render,
    redirect,
    render_to_response
)
from django.http import Http404
from django.contrib.auth import login, logout
from .forms import (
    ShortUrlForm,
    SignUpForm,
    SignInForm,
    RestorationForm
)
from .url_utils import generate_short_url
from .models import (
    Url,
    UrlConfirmation,
    sign_up,
    get_user
)


def index(request):
    session_data = request.session.get('data')
    response_data = {}
    if session_data:
        response_data.update(**session_data)
        request.session.pop('data')
    if request.method == 'POST':
        if 'generate_url' in request.POST:
            form = ShortUrlForm(request.POST)
            short_url = ''
            if form.is_valid():
                author = request.user if request.user.is_authenticated else None
                short_url = generate_short_url(request.POST['long_url'], request.POST['custom_url'], author)
                short_url = '/'.join((request.get_host(), short_url))
            response_data.update(shortener_form=form, short_url=short_url)
        elif 'sign_up' in request.POST:
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = sign_up(form.cleaned_data, request)
                form = None
                response_data.update(success_registration=True, email=user.email)
            response_data.update(sign_up_form=form)
        elif 'sign_in' in request.POST:
            form = SignInForm(request.POST)
            if form.is_valid():
                user = get_user(form.cleaned_data)
                if user.is_active:
                    login(request, user)
                else:
                    response_data.update(email=user.email, email_confirmation=True)
                form = None
            response_data.update(sign_in_form=form)
        elif 'logout' in request.POST:
            logout(request)
        elif 'restoration' in request.POST:
            form = RestorationForm(request.POST)
            if form.is_valid():
                form = None
            else:
                response_data.update(restoration=True)
            response_data.update(restoration_form=form)

    return render(request, 'shortener/index.html', {'user': request.user,
                                                    'response_data': response_data})


def redirect_short_url(request, url):
    url_object = Url.get_url_object(url)
    if url_object:
        return redirect(url_object.long_url)
    raise Http404


def get_statistics(request, url):
    if request.user.is_authenticated:
        url_data = Url.get_url_object(short_url=url, author=request.user)
        if url_data:
            return render(request, 'shortener/url_statistics.html', {'user': request.user})
    raise Http404


def activate_account(request):
    key = request.GET.get('key', '')
    if key:
        url = UrlConfirmation.get_url(key)
        if url:
            url.user.is_active = True
            url.user.save()
            UrlConfirmation.delete_url(url.user)
            login(request, url.user)
            request.session['data'] = {'congratulation': True}
            return redirect('index')
        raise Http404
    raise Http404


def handler404(request, exception, template_name="404.html"):
    response = render_to_response("404.html")
    response.status_code = 404
    return response
