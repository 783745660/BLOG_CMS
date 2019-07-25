#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/7/23 12:54'

import xadmin
from .models import Image

class ImageAdmin(object):
    list_display = ('user','title','url','image','created')
    list_filter = ('user','title')

xadmin.site.register(Image,ImageAdmin)

