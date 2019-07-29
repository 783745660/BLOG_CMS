#coding=utf-8
"""Online_Blog_CMS URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url,include
from extra_apps import xadmin
from django.views.generic import TemplateView
from django.views.static import serve

from .settings import MEDIA_ROOT


urlpatterns = [
    url(r'^xadmin/',xadmin.site.urls),
    url(r'^blog/',include('blog.urls')), #以blog开头的url会分发到blog.urls下
    url(r'^account/',include('account.urls')),
    url(r'^article/',include('article.urls')),
    url(r'^$',TemplateView.as_view(template_name='home.html'),name='home'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}), #为media中的每一个静态图片配置好url，可以在前端中用image.url获取图片
    url(r'^image/',include('image.urls')),
    url(r'^course/',include('course.urls')),
]
