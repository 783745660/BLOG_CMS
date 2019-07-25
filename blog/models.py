#coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Create your models here.

class BlogArticles(models.Model):
    '''
    创建models.Model的子类为文章数据表对象，类属性对应该表的字段
    '''
    title = models.CharField(max_length=300,verbose_name=u'标题')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts',verbose_name=u'作者')
    content = models.TextField(verbose_name=u'内容')
    publish_time = models.DateTimeField(default=timezone.now,verbose_name=u'发布时间') #这里使用now函数对象的原因是避免在该类被编译的时候就运行该函数，而是该类被实例化的时候运行

    class Meta:
        verbose_name_plural = verbose_name = u'博客管理'
        ordering = ("-publish_time",) #这里的ordering必须是一个元组或列表对象

    def __unicode__(self):
        return self.title      #在后台管理中显示文章的标题

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})
