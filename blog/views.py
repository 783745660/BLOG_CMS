#coding=utf-8

from django.shortcuts import render

from .models import BlogArticles
# Create your views here.


def blog_index(request):
    blogs = BlogArticles.objects.all()
    contexts = {'blogs':blogs}
    return render(request, 'blog/index.html', contexts)

def blog_article(request,pk):
    article = BlogArticles.objects.get(pk=pk)
    contexts = {'article':article}
    return render(request,'blog/content.html',contexts)
