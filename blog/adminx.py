#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/7/18 9:32'

import xadmin
from .models import BlogArticles

# Register your models here.

class BlogArticleAdmin(object):
    list_display = ('title','author','content','publish_time')
    list_filter = ('publish_time','author')
    search_fields = ('title','content')
    date_hierarchy = 'publish_time'
    ordering = ['publish_time','author']


xadmin.site.register(BlogArticles,BlogArticleAdmin)