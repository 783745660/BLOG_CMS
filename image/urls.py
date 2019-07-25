#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/7/22 20:29'

from django.conf.urls import url
import views

app_name = 'image'

urlpatterns = [
    url(r'^list-images/$',views.list_images,name='list_images'),
    url(r'^upload-image/$',views.upload_image,name='upload_image'),
    url(r'^del-image/$',views.del_image,name='del_image'),
    url(r'^falls-images/$',views.falls_images,name='falls_images'),
]
