#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/7/20 16:50'

from django.shortcuts import render,get_object_or_404,HttpResponse,redirect,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import ArticleColumn,ArticlePost
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models import Q #搜索

from .form import CommentForm


#用于博客展示


def articles_titles(request,username=None):
    '''
    给网民展示博客,不用检查用户是否登陆，
    :param request:
    :return:
    '''
    userinfo = None
    user = None
    if username:
        user = User.objects.get(username=username)
        articles_title = ArticlePost.objects.filter(author=user)
        try:
            userinfo = user.userinfo
        except:
            userinfo = None
    else:
        articles_title = ArticlePost.objects.all()

    paginator = Paginator(articles_title,4) #获得一个分页对象，每页最多4个博客标题对象
    page_number = request.GET.get('page')   #从页面获取当前的页码
    try:
        current_page = paginator.page(page_number) #生成当前页的对象
        current_page_articles = current_page.object_list #获取当前页的博客
    except PageNotAnInteger:
        current_page = paginator.page(1)
        current_page_articles = current_page.object_list #页码非整，获取第一页博客
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        current_page_articles = current_page.object_list #页码为空，获取最后的页码的博客

    contexts = {'articles':current_page_articles,
                'page':current_page}

    contexts2 = {'articles':current_page_articles,
                'page':current_page,
                 'userinfo':userinfo,'user':user}
    if username:
        return render(request,'article/list/author_articles.html',context=contexts2)

    return render(request, 'article/list/articles_titles_list.html', context=contexts)


def article_content(request,id,slug):
    '''
    给每篇博客加内容链接，此外，该函数每被调用一次，该博客的浏览量加1
    :param request:
    :param id:
    :param slug:
    :return:
    '''
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    article_tags_ids = article.article_tag.values_list('id', flat=True)
    similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count('article_tag')).order_by('-same_tags', '-created')[:5]
    comment_form = CommentForm()
    article.increase_views()

    context = {'article':article,
               'comment_form':comment_form,
               'similar_articles':similar_articles,
               }
    return render(request, 'article/list/articles_content.html', context=context)


def article_comment(request,id,slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.commentator = request.user
            new_comment.save()
            return HttpResponseRedirect(reverse('article:article_content',kwargs={'id':id,'slug':slug}))
    else:
        comment_form = CommentForm()
    context = {'article':article,
               'comment_form':comment_form,
               }
    return render(request,'article/list/articles_content.html',context=context)





@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def like_article(request):
    '''
    给博客点赞
    :param request:
    :return:
    '''
    article_id = request.POST.get('id')
    action = request.POST.get('action')
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action == 'like':
                article.user_like.add(request.user)
                return HttpResponse('1')
            else:
                article.user_like.remove(request.user)
                return HttpResponse('2')
        except:
            return HttpResponse('no')

        
def search(request):
    '''
    简单搜索
    :param request:
    :return:
    '''
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = "请输入关键词"
        return render(request, 'article/list/articles_titles_list.html', {'error_msg': error_msg})

    search_articles = ArticlePost.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    paginator = Paginator(search_articles,4) #获得一个分页对象，每页最多4个博客标题对象
    page_number = request.GET.get('page')   #从页面获取当前的页码
    try:
        current_page = paginator.page(page_number) #生成当前页的对象
        current_page_articles = current_page.object_list #获取当前页的博客
    except PageNotAnInteger:
        current_page = paginator.page(1)
        current_page_articles = current_page.object_list #页码非整，获取第一页博客
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        current_page_articles = current_page.object_list #页码为空，获取最后的页码的博客

    contexts = {'articles':current_page_articles,
                'page':current_page,
                }
    return render(request,  'article/list/articles_titles_list.html',contexts)
