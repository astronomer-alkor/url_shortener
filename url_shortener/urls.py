"""url_shortener URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shortener.views import (
    index,
    redirect_short_url,
    get_statistics,
    activate_account
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('<url>', redirect_short_url, name='redirect_short_url'),
    path('<url>/statistics', get_statistics, name='get_statistics'),
    path('activation/', activate_account, name='activate_account'),
]
