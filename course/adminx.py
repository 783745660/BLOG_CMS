#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/7/23 16:28'

import xadmin
from .models import Lesson

class LessonAdmin(object):
    list_display = ('user','course','title','video','attach','created','order')
    list_filter = ('user','title')

xadmin.site.register(Lesson,LessonAdmin)