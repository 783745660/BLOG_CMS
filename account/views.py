#coding=utf-8

from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib.auth import authenticate,login    #Django内置的用户登录和认证方法
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import UserProfile,UserInfo
from .forms import LoginForm,RegisterationForm,UserProfileForm,UserInfoForm,UserForm


# Create your views here.

# def user_login(request):
#     '''
#     用户登录逻辑，如果请求方法为get,则为浏览器响应一个登录表单；如果请求方法为post,则为其响应登录状态
#     :param request:
#     :return:
#     '''
#     if request.method == 'POST':
#         login_form = LoginForm(request.POST)
#         if login_form.is_valid():
#             cd = login_form.cleaned_data  #字典类型
#             user = authenticate(username=cd['username'],password=cd['password']) #验证表单账号是否在后台被注册
#             if user:
#                 login(request,user)
#                 return HttpResponse('Welcome You.You have been authenticated successfully')
#             else:
#                 return HttpResponse('Sorry.Your username or password is not right,please try again')
#         else:
#             return HttpResponse('Invalid login,please try again')
#
#     if request.method == 'GET':
#         login_form = LoginForm()
#         contexts = {'login_form':login_form}
#         return render(request,'account/login.html',contexts)

def register(request):
    if request.method == 'POST':
        user_form = RegisterationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid()*userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            UserInfo.objects.create(user=new_user)
            return HttpResponseRedirect(reverse("account:login"))
        else:
            return HttpResponse("Sorry, Your username or password or other filed is not right.")
    else:
        user_form = RegisterationForm()
        profile_form = UserProfileForm()
        contexts = {'form':user_form,
                    'profile':profile_form}
        return render(request,'account/register.html',contexts)


@login_required(login_url='/account/login/')
def myself(request):
    '''
    如果用户在没有登录的情况下访问这些视图函数对于的url也会首先跳转到登录页面，登录成功后自动跳转到之前访问的url
    这里的意思是只从数据表User,UserProfile,UserInfo中取出当前的登录用户记录
    :param request:
    :return:
    '''
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    contexts = {'user':user,
                'userprofile':userprofile,
                'userinfo':userinfo,
                }
    return render(request,'account/myself.html',contexts)


@login_required(login_url='/account/login/')
def myself_edit(request):
    '''
    从数据表User,UserProfile,UserInfo中取出当前的登录用户记录,并通过Post方法实例化各form表单，
    从表单中取出用户数据，赋值给用户字段后保存，表单提交后，将页面重定向到用户个人信息页面
    :param request:
    :return:
    '''
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            user.save()
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('/account/my-information/') #无论表单对或错都定向到我的信息页面
    else:
        user_form = UserForm(instance=request.user)
        initial_profile = {"birth":userprofile.birth, "phone":userprofile.phone}
        userprofile_form = UserProfileForm(initial=initial_profile)
        initial_info = {"school":userinfo.school, "company":userinfo.company, "profession":userinfo.profession, "address":userinfo.address, "aboutme":userinfo.aboutme}
        userinfo_form = UserInfoForm(initial= initial_info)
        contexts = {"user_form":user_form, "userprofile_form":userprofile_form, "userinfo_form":userinfo_form}
        return render(request, "account/myself_edit.html", contexts)


@login_required(login_url='/account/login/')
def my_image(request):
    if request.method == 'POST':
        img = request.POST['img']  #与 request.POST.get('img')的区别是如果找不到该键，前者报错，而后者不报错
        userinfo = UserInfo.objects.get(user=request.user.id)
        print len(img)
        userinfo.image = img
        userinfo.save()
        return HttpResponse('1')
    else:
        return render(request,'account/imagecrop.html',)


@login_required(login_url='/account/login/')
@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES.get('docfile')
        print image
        userinfo = UserInfo.objects.get(user=request.user.id)
        userinfo.image = image
        userinfo.save()
        return redirect('/account/my-information') #重定向到用户信息主页
    else:
        return HttpResponse('ERROR!')
