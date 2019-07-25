#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/7/19 11:53'

import xadmin
from .models import UserProfile,UserInfo


class UserProfileAdmin(object):
    list_display = ('user','birth','phone')
    list_filter = ('phone',)
    search_fileds = ('user','phone')


class UserInfoAdmin(object):
    list_display = ('user','school','address','profession','aboutme','modify_time')
    list_filter = ('school','address','profession')
    search_fileds = ('user','school')

xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(UserInfo,UserInfoAdmin)