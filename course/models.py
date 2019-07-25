#coding=utf-8

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

from slugify import slugify

from .fields import OrderField


# Create your models here.


class Course(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='course_user',verbose_name=u'用户')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = verbose_name = u'用户课程'

    def save(self,*args,**kwargs):
        '''
        重写model类的save()方法
        :param args:
        :param kwargs:
        :return:
        '''
        self.slug = slugify(self.title)
        super(Course,self).save(*args,**kwargs)

    def __unicode__(self):
        return self.title


def user_directory_path(instance,filename):
    '''
    定义用户上传视频和文件的本地目录
    :param instance:
    :param filename:
    :return:
    '''
    return 'course/user_{0}/{1}'.format(instance.user.id,filename)


class Lesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_user', verbose_name=u'用户')
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='lesson',verbose_name=u'所属课程')
    title = models.CharField(max_length=200,verbose_name=u'标题')
    video = models.FileField(upload_to=user_directory_path,verbose_name=u'视频')
    description = models.TextField(blank=True,null=True)
    attach = models.FileField(blank=True,null=True,upload_to='attachs',verbose_name=u'附件')
    created = models.DateTimeField(auto_now_add=True)
    order = OrderField(blank=True,null=True,for_fields=['course'],verbose_name=u'顺序')

    class Meta:
        ordering = ['order']
        verbose_name_plural = verbose_name = u'课程内容'

    def __unicode__(self):
        return '{}.{}'.format(self.order,self.title)


