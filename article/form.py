#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/7/19 19:07'

from django import forms
from .models import ArticleColumn,ArticlePost,Comment,ArticleTag

class ArticleColumnForm(forms.ModelForm):
    '''
    在页面添加博客栏目，并将column字符数据写入到ArticleColumn数据表中
    '''
    class Meta:
        model = ArticleColumn
        fields = ('column',)

class ArticlePostForm(forms.ModelForm):
    '''
    在页面发布博客，将填写的标题和内容更新到数据表ArticlePost
    '''
    class Meta:
        model = ArticlePost
        fields = ('title','body')


class CommentForm(forms.ModelForm):
    '''
    评论表单
    '''
    class Meta:
        model = Comment
        fields = ('body',)


class ArticleTagForm(forms.ModelForm):
    '''
    博客标签表单
    '''
    class Meta:
        model = ArticleTag
        fields = ('tag',)