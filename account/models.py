#coding=utf-8
from __future__ import unicode_literals

from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True,verbose_name=u'用户名')
    birth = models.DateField(blank=True,null=True,verbose_name=u'生日')
    phone = models.CharField(max_length=20,null=True,verbose_name=u'联系方式')
    resgister_time = models.DateTimeField(default=timezone.now,verbose_name=u'注册日期')

    class Meta:
        verbose_name_plural = verbose_name = u'注册信息'

    def __unicode__(self):
        return self.user.username


class UserInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True,verbose_name=u'用户')
    school = models.CharField(max_length=100,blank=True,null=True,verbose_name=u'学校')
    company = models.CharField(max_length=100,blank=True,null=True,verbose_name=u'公司')
    address = models.CharField(max_length=100,blank=True,null=True,verbose_name=u'地址')
    profession = models.CharField(max_length=100,blank=True,null=True,verbose_name=u'职业')
    aboutme = models.TextField(blank=True,null=True,verbose_name=u'简介')
    modify_time = models.DateTimeField(default=timezone.now,verbose_name=u'修改日期')
    image = models.ImageField(null=True,blank=True,upload_to='images/account/%Y/%m/%d')

    class Meta:
        verbose_name_plural = verbose_name = u'个人信息'

    def __unicode__(self):
        return self.user.username
