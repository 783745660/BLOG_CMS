#coding=utf-8


import json

from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from .models import ArticleColumn,ArticlePost,ArticleTag
from .form import ArticleColumnForm,ArticlePostForm,ArticleTagForm


# Create your views here.
#下面的所有方法都是用于用户管理自己的博客


@login_required(login_url='/account/login/')
@csrf_exempt    #解决csrf攻击
def article_column(request):
    '''
    用户添加博客栏目
    GET:从数据表中读取该用户的栏目，以及展示要填写表的单页面
    POST:从提交的post的表单中读取数据，如果填写的表单数据已存在用户栏目中返回前端'1',否则创建文章栏目
    :param request:
    :return:
    '''
    if request.method == 'GET':
        user = request.user
        columns = ArticleColumn.objects.filter(user=user) #读取用户栏目
        columns_form = ArticleColumnForm() #实例化栏目表单
        context = {'columns':columns,  #显示栏目
                    'columns_form':columns_form, #显示表单
                    }
        return render(request,'article/column/article_column.html',context=context)

    if request.method == 'POST':
        column_name = request.POST['column'] #填写的栏目名称
        try:
            columns = ArticleColumn.objects.filter(user_id=request.user.id,column=column_name)
            if columns:
                return  HttpResponse('2') #ajax中表示添加失败
        except Exception as e:
            print e
        else:
            ArticleColumn.objects.create(user=request.user,column=column_name) #在当前用户下创建一个目录名
            return HttpResponse('1') #ajax中表示重新加载之前显示用户栏目页面


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def rename_article_colum(request):
    '''
    用户修改栏目名称
    :param request:
    :return:
    '''
    column_name = request.POST['column_name']
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id) #读取当前数据行
        line.column = column_name #将修改的栏目名赋值为该行column字段
        line.save()
        return HttpResponse('1')
    except:
        return HttpResponse('2')


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article_column(request):
    '''
    用户删除栏目
    :param request:
    :return:
    '''
    column_id = require_POST['column_id'] #当前请求的栏目id
    try:
        line = ArticleColumn.objects.get(id=column_id)  #从数据表中定位到该栏目记录
        line.delete()  #删除本行
        return HttpResponse('1') #表示删除成功
    except:
        return HttpResponse('2') #表示删除失败


@login_required(login_url='/account/login')
@csrf_exempt
def article_post(request):
    '''
    用户发布博客
    :param request:
    :return:
    '''
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST) #从前台得到request.POST内的数据，为一个字典，键就是form中字段，所以才能够实例化
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                #new_article.column = ArticleColumn.objects.filter(user=request.user,id=request.POST['column_id'])
                new_article.column = request.user.article_column.get(id=request.POST['column_id']) #外键的作用` ``
                new_article.save()
                tags = request.POST['tags']
                if tags:
                    for atag in json.loads(tags):  #json()模块将禽前端传过来的json格式的tags转换为列表
                        tag = request.user.tag.get(tag=atag)
                        new_article.article_tag.add(tag)
                return HttpResponse('1')

            except Exception as e:
                print e   #dubug过程中不执行 new_article.save() 然后用此方法捕获异常
                return HttpResponse('2')
        else:
            print article_post_form.errors
            return HttpResponse('3')

    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        article_tags = request.user.tag.all()
        context = {'article_post_form':article_post_form,
                    'article_columns':article_columns,
                   'article_tags':article_tags,
                   }
        return render(request,'article/column/article_post.html',context=context)



@login_required(login_url='/account/login/')
def article_list(request):
    '''
    用户点击博客列表展示博客标题列表,并展示分页
    :param request:
    :return:
    '''
    articles_list = request.user.article.all()
    paginator = Paginator(articles_list,4) #获得一个分页对象，每页最多4个博客标题对象
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
    context = {'articles':current_page_articles,
                'page':current_page}
    return render(request,'article/column/article_list.html',context=context)


@login_required(login_url='/accout/login')
def article_detail(request,id,slug):
    '''
    给博客列表中的标题增加详情链接
    :param request:
    :param id:
    :param slug:
    :return:
    '''
    #article = ArticlePost.objects.filter(id=id,slug=slug)
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    context = {'article':article}
    return render(request,'article/column/article_detail.html',context=context)


@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article(request):
    '''
    用户删除博客
    :param request:
    :return:
    '''
    article_id = request.POST['article_id']
    try:
        article = request.user.article.get(id=article_id)
        article.delete()
        return HttpResponse('1')
    except Exception as e:
        print e
        return HttpResponse('2')


@login_required(login_url='/account/login')
#@require_POST 去掉不允许get方法装饰器
@csrf_exempt
def redit_article(request,id):
    '''
    用户编辑已发布的博客
    :param request:
    :param id:
    :return:
    '''
    if request.method == 'GET':
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id=id)
        this_article_column = article.column
        this_article_form = ArticlePostForm(initial={'title':article.title})
        context = {'article_columns':article_columns,
                    'article':article,
                    'this_article_form':this_article_form,
                    'this_article_column':this_article_column}
        return render(request,'article/column/redit_article.html',context=context)
    else:
        redit_article = ArticlePost.objects.get(id=id)
        try:
            redit_article.column = request.user.article_column.get(id=request.POST['column_id'])
            redit_article.title = request.POST['title']
            redit_article.body = request.POST['body']
            redit_article.save()
            return HttpResponse('1')
        except:
            return HttpResponse('2')


@login_required(login_url='/account/login')
@csrf_exempt
def article_tag(request):
    '''
    管理博客标签
    :param request:
    :return:
    '''
    if request.method == "GET":
        article_tags = ArticleTag.objects.filter(author=request.user)
        article_tag_form = ArticleTagForm()
        return render(request, "article/tag/tag_list.html",
                      {"article_tags": article_tags, "article_tag_form": article_tag_form})

    if request.method == "POST":
        tag_post_form = ArticleTagForm(data=request.POST)
        if tag_post_form.is_valid():
            try:
                new_tag = tag_post_form.save(commit=False)
                new_tag.author = request.user
                new_tag.save()
                return HttpResponse("1")

            except Exception as e:
                print e
                return HttpResponse("the data cannot be save.")
        else:
            return HttpResponse("sorry, the form is not valid.")



@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article_tag(request):
    tag_id = request.POST['tag_id']
    try:
        tag = ArticleTag.objects.get(id=tag_id)
        tag.delete()
        return HttpResponse('1')

    except Exception as e:
        print e
        return HttpResponse('2')