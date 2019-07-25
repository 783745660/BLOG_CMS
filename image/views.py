#coding=utf-8

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .form import ImageForm
from .models import Image

# Create your views here.


@login_required(login_url='/account/login/')
@csrf_exempt
@require_POST
def upload_image(request):
    '''
    接收前台提交的图片url及其他信息,调用在ImageForm中重写的save方法，
    :param request:
    :return:
    '''
    form = ImageForm(data=request.POST) #在前台定义一个request.POST内的数据是一个photo,一个字典键值对,里面的键就是form的字段，值是用户填写的内容
    if form.is_valid():
        try:
            new_item = form.save(commit=False) #调用我们在ImageForm中重写的save方法得到一个待保存的form对象，这里把commit定义为False，那么
            new_item.user = request.user
            new_item.save()  #保存到数据库  #再次调用重写的save()方法，该方法中的关键字commit默认为True,将其保存至数据库
            return JsonResponse({'status':'1'})
        except Exception as e:
            print e
            return JsonResponse({'status':'0'})
    else:
        print form.errors



@login_required(login_url='account/login/')
@require_POST
@csrf_exempt
def del_image(request):
    '''
    删除图片视图函数
    :param request:
    :return:
    '''
    image_id = request.POST['image_id']  #从前端得到此图片id
    try:
        image = Image.objects.get(id =image_id) #从数据库中锁定图片
        image.delete() #删除图片
        return JsonResponse({'status':1})
    except Exception as e:
        print e
        return JsonResponse({'status':0})


@login_required(login_url='/account/login/')
def list_images(request):
    '''
    在前端展示用户提交的图片
    :param request:
    :return:
    '''
    images = Image.objects.filter(user=request.user)
    # 该方法是利用image中的外键user取到该登录用户下的所有图片,但缺点是一旦该用户没有图片就会报错
    # images = request.user.images
    return render(request,'images/list_images.html',{'images':images})



def falls_images(request):
    '''
    用瀑布流方式展示图片
    :param request:
    :return:
    '''
    images = Image.objects.all()
    return render(request,'images/falls_images.html',{'images':images})

