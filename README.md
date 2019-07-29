# BLOG_CMS
基于Django1.9完成的在线博客管理系统

## 记录一下部署djnago是遇到的坑
在配置nginx时候，由于没有设置好nginx的启动权限，导致在sites-available中定义的配置文件不起作用，因此需要在nginx的安装位置基于root权限,另外还一小坑就是在配置文件中将proxy_下划线漏掉，花了很近一天的时间..
由于用nginx监听80端口，而Linux下开启1024以下端口需要root权限，因此在普通用户下开启nginx需要给nginx加root权限
chown root nginx
chmod u+s nginx
## 项目步骤说明
该项目可以实现一个博客问答社区，主要功能用户发表文章，文章评论及文章分类等功能，项目由 python 的第三方 web 开源框架 Django 开发完成。
## 1. 项目开发环境
本教程写作时开发环境的系统平台为 Windows 10 （64 位），Python 版本为2.7.16（64 位），Django 版本为 1.9
#### 1) 安装Python
去Python官网下载windows版本，双击后完成安装(记得勾选将其添加到系统路径)，打开cmd，输入python，验证python书否安装成功

####  2) 使用虚拟环境 Virtualenv
Virtualenv 是一个 Python 工具，使用它可以创建一个独立于原来的 Python 环境，从而避免新安装的 Python 库与之前旧的库发生不必要的冲突。安装 virtualenv 库
```
pip install virtualenv
```
安装 virtualenv 后创建一个本地虚拟环境，并指定当前虚拟环境的目录路径
```
virtualenv project_env
```
激活虚拟环境
```
windows:
project_env\Scripts\activate
```
```
Linux 下没有 Scripts\ 这个目录，取而代之的是 bin/ 目录
$ source project_env/bin/activate
```
#### 3）安装 django 1.9
```
pip install django==1.9
```

## 2. 创建博客项目
基本的开发环境已经具备，下面开始创建博客项目
#### 1) 在 pycharm 专业版中配置好之前的项目解释器和虚拟环境，并创建 django 项目工程
```
blogproject\
    manage.py
    blogproject\
        __init__.py
        settings.py
        urls.py
        wsgi.py
```
#### 2) 修改 settings.py 中时区和语言配置
```
blogproject/blogproject/settings.py

## 其它配置代码...

# 把英文改为中文
LANGUAGE_CODE = 'zh-hans'

# 把国际时区改为中国时区
TIME_ZONE = 'Asia/Shanghai'

## 其它配置代码...
```
#### 3) 建立博客应用，一个项目包含不止一种功能，我们将实现不同功能的代码发在一个app应用下
使用 manage.py 的 startapp 命令创建了一个 blog 应用，创建后的app目录为
```
blog\
    __init__.py
    admin.py
    apps.py
    migrations\
        __init__.py
    models.py
    tests.py
    views.py
```
每创建一个项目的app，都需要将其注册到项目工程下的 配置文件 settings.py 中
```
blogproject/blogproject/settings.py

## 其他配置项...

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog', # 注册 blog 应用
]

## 其他配置项...
```
#### 4) 编写数据模型，并将其迁移到数据库，形成数据库文件格式
 Django 为我们提供了一套 ORM（Object Relational Mapping）系统，即 Django 把那一套数据库的语法转换成了 Python 的语法形式，我们只要写 Python 代码就可以了，Django 会把 Python 代码翻译成对应的数据库操作语言。
 ```
 blog/models.py

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
  	...
  	...
 ```
 编写了博客数据库模型的代码之后，Django需要将其翻译成数据库语言，分别运行 python manage.py makemigrations 和 python manage.py migrate 命令：
 ```
 python manage.py makemigrations 
 ```
Django 在 blog 应用的 migrations\ 目录下生成了一个 0001_initial.py 文件，这个文件是 Django 用来记录我们对模型做了哪些修改的文件
 ```
 python manage.py migrate 
 ```
执行 python manage.py migrate 命令之后，Django 通过检测应用中 migrations\ 目录下的文件，得知我们对数据库做了哪些操作，然后它把这些操作翻译成数据库操作语言，从而把这些操作作用于真正的数据库。
#### 5）配置数据库
django默认使用的数据库是python自带的轻巧型数据库SQLite3， 我们可以在settings.py中配置其他数据库:
```
blogproject/settings.py

## 其它配置选项...
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
## 其它配置选项...
```
## 3. 完成 Django 处理 http 请求先关工作
 Django 通过绑定 URL 与视图函数的方式，来接受浏览器的 HTTP 请求。当用户输网址后，django调用与其绑定在一起的视图函数，完成http响应，我们需要在视图函数中编写响应逻辑代码。
#### 1）首先在 blog 应用的目录下创建一个 urls.py 文件
在blog/urls.py中写入这些代码:
```
blog/urls.py

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
```
在 blog 应用下的 views.py 中编写响应逻辑代码
```
blog/views.py

from django.http import HttpResponse

def index(request):
    return HttpResponse("欢迎访问我的博客首页！")
 ```
#### 2) 将blog应用下的 urls.py 包含到 blogproject\urls.py 中
Django 匹配 URL 模式是在 blogproject\ 目录（即 settings.py 文件所在的目录）的 urls.py 下的，Django并不知道 blog/urls.py 的存在，因此，我们需要将其包含到项目下的urls.py中
```
blogproject/urls.py

"""
一大段注释
"""

from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('blog.urls')),
]
```
运行 python manage.py runserver 打开开发服务器，在浏览器输入开发服务器的地址 http://127.0.0.1:8000/, 可以看到 Django 返回的内容了。
## 4 项目部署
使用 Nginx 和 Gunicorn 部署 Django 博客
### 服务器准备
#### 1) 购买阿里云服务器，可以选择轻量级应用服务器，并选择Linux操作系统
#### 2）购买域名并在阿里云操作台完成域名解析服务
#### 3）注册域名，完成备案申请
### 搭建服务器
由于本人在windows上开发该Django项目，而服务器是部署在云端的，我们需要在windows平台上使用远程登录工具 xshell 来操作服务器配置
#### 1) 使用xshell远程连接服务器
#### 2) 新建一个用户
如果是一台全新服务器的话，通常我们是以 root 用户登录的。但在 root 下部署代码不安全，最好是建一个新用户
```
增加用户
root@localhost:~# useradd -m -s /bin/bash username

把新创建的用户加入超级权限组
root@localhost:~# usermod -a -G sudo username

为用户配置密码
root@localhost:~# passwd password

切换到创建的新用户
root@localhost:~# su - username
```
#### 3）在服务器上安装必要的软件
先更新系统软件
ubuntu 升级软件：
```
sudo apt-get update 更新源
sudo apt-get upgrade 更新已安装的包

```
接下来就可以安装必要的软件
```
username@localhost:~$ sudo apt-get install nginx
username@localhost:~$ sudo apt-get install git python3 python3-pip
username@localhost:~$ sudo pip3 install virtualenv
```
启动Nginx服务
Nginx 是用来处理静态文件请求的，包括图片、css、js 等存在服务器某个文件夹下的静态文件，而显示文章的详情信息由django处理。Nginx安装好之后，并且已经把域名和服务器 IP 绑定了。运行下面的命令启动 Nginx 服务：
```
 sudo service nginx start
```
可在浏览器中输入域名，检测Nginx是否启动成功
### 代码部署
#### 1）修改项目配置代码
为让Nginx处理静态文件，将项目所有的静态文件放入到文件夹static中
```
blogproject/settings.py

# 其他配置...

STATIC_URL = '/static/'
# 加入下面的配置
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  #STATIC_ROOT 指明了静态文件的收集目录
```
关闭debug模式，并配置允许访问的域名列表
```
blogproject/settings.py

DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost ', 域名]
```
新建一个项目文件夹project，将项目代码拉到该文件夹下，并安装项目依赖
```
 pip install -r requirements.txt
```
将项目中的静态文件收集到static文件夹下，以方便Nginx访问
```
python manage.py collectstatic
```
生产数据库文件
```
python manage.py migrate
```
#### 2) 配置Nginx
在服务器的/etc/nginx/sites-available/目录下新建一个配置文件demo_site，写入如下配置
```
/etc/nginx/sites-available/demo_site

server {
    charset utf-8;
    listen 80;
    server_name songwen.top;  #域名

    location /static { 
        alias /home/username/project/song_qa_public/static;   #静态文件目录
    }

    location / { 
        proxy_set_header Host $host;                  
        proxy_pass http://unix:/tmp/songwen.top.socket;
    }
}
```
然后把这个配置文件放入到启用网站列表中，被启用网站的目录在 /etc/nginx/sites-enabled/，从 sites-available/ 目录下发送了一个配置文件的快捷方式到 sites-enabled/ 目录
```
sudo ln -s /etc/nginx/sites-available/demo_site  /etc/nginx/sites-enabled/demo_site
```
#### 3) 使用 Gunicorn 来管理进程
安装 Gunicorn：
```
pip install gunicorn
```
启用gunicorn
```
 gunicorn --bind unix:/tmp/songwen.top.socket  blogproject.wsgi:application
```
输入域名，部署成功

