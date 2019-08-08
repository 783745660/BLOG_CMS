#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/7/19 19:15'

from django.conf.urls import url

from . import views,list_views


app_name = 'article'

urlpatterns = [
    url(r'^article-column/$',views.article_column,name='article_column'),
    url(r'^rename-column/$',views.rename_article_colum,name='rename_article_column'),
    url(r'^del-column/$',views.del_article_column,name='del_article_column'),
    url(r'^article-post/$',views.article_post,name='article_post'),
    url(r'^article-list/$',views.article_list,name='article_list'),
    url(r'^article-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$',views.article_detail,name='article_detail'),
    url(r'^del-article/$',views.del_article,name='del_article'),
    url(r'^redit-article/(?P<id>\d+)/$',views.redit_article,name='redit_article'),
    url(r'^list-articles-titles/$',list_views.articles_titles,name='articles_titles'),
    url(r'^article-content/(?P<id>\d+)/(?P<slug>[-\w]+)/$',list_views.article_content,name='article_content'),
    url(r'^article-comment/(?P<id>\d+)/(?P<slug>[-\w]+)/$',list_views.article_comment,name='article_comment'),
    url(r'^list-articles-titles/(?P<username>\w+)/$',list_views.articles_titles,name='author_articles'),
    url(r'^like-article/$',list_views.like_article,name='like_article'),
    url(r'^article-tag/$',views.article_tag,name='article_tag'),
    url(r'^del_article_tag/$',views.del_article_tag,name='del_article_tag'),
    url(r'search/$',list_views.search,name='search'),
]
