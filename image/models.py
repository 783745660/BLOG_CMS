#coding=utf-8

from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import  User

from slugify import  slugify


class Image(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='images',verbose_name=u'用户') #可以通过user.images找到该用户的所有图片
    title = models.CharField(max_length=300,verbose_name=u'标题')
    url = models.URLField() #与CharField的区别是这个的字符串长度最大为200
    slug = models.SlugField(max_length=500,blank=True,null=True,verbose_name=u'英文标题')
    description = models.TextField(verbose_name=u'图片描述')
    created = models.DateField(auto_now_add=True,db_index=True,verbose_name=u'创建时间') #该类的实例被创建之后时间字段会自动生成，db_index表示以该字段为索引
    image = models.ImageField(upload_to='CollectionImage/%Y/%m/%d',verbose_name=u'图片地址')

    class Meta:
        verbose_name_plural = verbose_name = u'图片管理'


    def __unicode__(self):
        return self.title


    def save(self,*args,**kwargs):
        self.slug = slugify(self.title) # 重写 将该实例的title字段转为英文-分割类型
        super(Image,self).save(*args,**kwargs)

