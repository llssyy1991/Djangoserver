"""webserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from webserver.view import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^first/',login),
    url(r'^second/',getmenu),
    url(r'^third/',get_order),
    url(r'^set_plan/',setplan),
    url(r'^show_plan/',show_menu),
    url(r'^show_order_sold/',show_all_order_unfinished),
    url(r'^show_user_order/',show_user_order)
]
