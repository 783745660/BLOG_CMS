#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/7/22 19:38'

from django import forms
from django.core.files.base import ContentFile
from slugify import slugify
import urllib2

from .models import Image


class ImageForm(forms.ModelForm):
    '''
    定义一个Image的表单,该表单为基于Image的数据模型，用于页面表单的数据验证和保存
    可保存的Image字段为title,url,description
    '''
    class Meta:
        model = Image
        fields = ('title','url','description')


    def clean_url(self):
        '''
        新内容，用于处理Image的url字段，如果上传的图片地址有非法扩展名就主动抛出异常
        :return:
        '''
        url = self.cleaned_data['url'] #通过该方法获取url字段的值
        vaild_extensions = ['jpg','ipeg','png'] #定义图片有效扩展名
        extension = url.rsplit('.',1)[1].lower() #处理上传的图片扩展名
        if extension not in vaild_extensions:
            raise forms.ValidationError('The given url does not match vaild image extension') #抛出异常
        return url


    def save(self,force_insert=False,force_update=False, commit=True):
        '''
        重写save()，给图片名称image_name为title.扩展名
        模拟用户，根据图片url得到图片并保存
        :param force_insert:
        :param force_update:
        :param commit:
        :return:
        '''
        image = super(ImageForm,self).save(commit=False)
        image_url = self.cleaned_data['url']    #经重写clean_url()后得到图片的url
        image_name = '{0}.{1}'.format(slugify(image.title),image_url.rsplit('.',1)[1].lower()) #将image的名字命名为title.扩展名
        response = urllib2.urlopen(image_url) #模拟用户输入url地址调用urlopen函数对请求的url返回一个response对象，有响应头，url等信息，类似于file对象，然后调用read()方法读取内容
        data = response.read() #解析到字符串
        image.image.save(image_name,ContentFile(data),save=False)  #将图片数据保存在本地
        if commit: #在view.py中的 upload_image()中我们将关键字commit其设置为False,直接返回一个image对象，并不将其保存至数据库中
            image.save()
        return image


