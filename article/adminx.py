#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/7/20 1:15'

from django.contrib import admin
import xadmin
from .models import ArticleColumn,ArticlePost,Comment

class ArticleColumnAdmin(object):
    list_display = ('column','creted','user')
    list_filter = ('column',)

class ArticlePostAdmin(object):
    list_display = ('author','title','column','updated')
    list_filter = ('column','title')

class CommentAdmin(object):
    list_display = ('article','commentator','created')
    list_filter = ('article',)


xadmin.site.register(ArticleColumn,ArticleColumnAdmin)
xadmin.site.register(ArticlePost,ArticlePostAdmin)
xadmin.site.register(Comment,CommentAdmin)