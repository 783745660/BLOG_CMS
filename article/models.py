#coding=utf-8

from __future__ import unicode_literals

from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User

from slugify import slugify

# Create your models here.

class ArticleColumn(models.Model):
    '''
    编写文章栏目数据模型
    '''
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='article_column',verbose_name=u'用户')
    column = models.CharField(max_length=200,verbose_name=u'栏目')
    creted = models.DateField(auto_now_add=True,verbose_name=u'创建时间')
    class Meta:
        verbose_name_plural = verbose_name = u'栏目管理'

    def __unicode__(self):
        return self.column



class ArticleTag(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tag')
    tag = models.CharField(max_length=200)
    class Meta:
        verbose_name_plural = verbose_name = u'博客标签'

    def __unicode__(self):
        return self.tag



class ArticlePost(models.Model):
    '''
    编写发布文章数据模型
    '''
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='article',verbose_name=u'作者')
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300)
    column = models.ForeignKey(ArticleColumn,on_delete=models.CASCADE,related_name='article_column')
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    user_like = models.ManyToManyField(User,related_name='articles_like',blank=True,null=True,verbose_name=u'点赞')
    viewnums = models.PositiveIntegerField(default=0)  #非负整数
    article_tag = models.ManyToManyField(ArticleTag,related_name='article_tag',blank=True,null=True,verbose_name=u'标签')
    class Meta:
        ordering = ('-updated',)
        index_together = (('id','slug'))

        verbose_name_plural = verbose_name = u'博客管理'
    def __unicode__(self):
        return self.title

    def save(self,*args,**kargs):
        self.slug = slugify(self.title)
        super(ArticlePost,self).save(*args,**kargs) #将博客中文标题转换为英文且中间用'-'分割

    def get_absolute_url(self):
        '''
        用在用户管理博客时给博客标题加链接时
        :return:
        '''
        return  reverse('article:article_detail',args=[self.id,self.slug])

    def get_content_url(self):
        '''
        游客可直接点击，无须登录
        :return:
        '''
        return reverse('article:article_content',args=[self.id,self.slug])

    def increase_views(self):
        '''
        记录博客浏览量
        :return:
        '''
        self.viewnums += 1
        self.save(update_fields=['viewnums'])



class Comment(models.Model):
    article = models.ForeignKey(ArticlePost,on_delete=models.CASCADE,related_name='comments',verbose_name=u'博客')
    commentator = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-created',)
        verbose_name_plural = verbose_name = u'评论管理'

    def __unicode__(self):
        return "Comment by {0} on {1}".format(self.commentator,self.article)


