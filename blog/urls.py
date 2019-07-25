#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/7/18 8:57'

from django.conf.urls import url

from . import views

app_name = 'blog'

urlpatterns = [
    url(r'^$',views.blog_index,name='index'), #这里的name是url的别名
    url(r'^(?P<pk>[0-9]+)/$',views.blog_article,name='detail')
]