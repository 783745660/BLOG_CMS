#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/7/21 10:59'


from django import template
from  django.db.models import Count

from article.models  import ArticlePost



#可以在模板中直接引用该模板标签，不需要在views.py中从数据库中读取数据后再传递给前端模板

register = template.Library()

@register.simple_tag
def total_articles():
    '''
    自定义模板标签，获取总博客数
    :return:
    '''
    return ArticlePost.objects.count()


@register.simple_tag
def author_total_articles(user):
    '''
    获取某位作者的博客数的模板标签，代表一个数字
    :param user:
    :return:
    '''
    return user.article.count()


@register.simple_tag
def most_views_articles(n=5):
    '''
    生成浏览量前5博客标签，代表的是一个集合对象，在article_content.html中必须先将其命别名,然后对其遍历
    :param n:
    :return:
    '''
    return ArticlePost.objects.order_by('viewnums')[:n]


@register.inclusion_tag('article/list/latest_articles.html')
def latest_articles(n=5):
    '''
    最近发布博客的标签，返回一个字典模板变量,用于article/list/latest_articles.html中，对其字典键对象变量，
    后续在article_content.html中可直接调用该模板标签
    :param n:
    :return:
    '''
    latest_articles = ArticlePost.objects.order_by('-created')[:n] # 从数据表中获取前n个最新发布的文章
    return {'latest_articles':latest_articles}


@register.simple_tag
def most_commented_articles(n=5):
    return ArticlePost.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:n]