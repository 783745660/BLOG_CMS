#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/7/18 15:15'

from django.conf.urls import url
from django.contrib.auth import views as auth_views  # 内置登录和退出方法
from . import views

app_name = 'account'
urlpatterns = [
    # url(r'^login/$',views.user_login,name='login'), #不使用自定义登录方法
    url(r'^login/$', auth_views.login, {'template_name': 'account/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'account/logout.html'}, name='logout'),
    url(r'^register/$',views.register,name='register'),
    url(r'^password-change/$',auth_views.password_change,{'template_name':'account/password_change_form.html',
                                                          'post_change_redirect':'/account/password-change-done',
                                                          },name='password_change'),

    url(r'password-change-done/$',auth_views.password_change_done,{'template_name':'account/password_changed_done.html',
                                                                   },name='password_change_done'),

    url(r'^password-reset/$', auth_views.password_reset, {"template_name": "account/password_reset_form.html",
                                                          "subject_template_name": "account/password_reset_subject.txt",
                                                          "email_template_name": "account/password_reset_email.html",
                                                          "post_reset_redirect": "/account/password-reset-done"},
        name="password_reset"),

    url(r'^password-reset-done/$', auth_views.password_reset_done,{"template_name": "account/password_reset_done.html"}, name="password_reset_done"),
    url(r'^password-reset-confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.password_reset_confirm,{"template_name": "account/password_reset_confirm.html",
         "post_reset_redirect": "/account/password-reset-complete"}, name="password_reset_confirm"),
    url(r'^password-reset-complete/$', auth_views.password_reset_complete,{"template_name": "account/password_reset_complete.html"}, name="password_reset_complete"),
    url(r'^my-information/$',views.myself,name='my_information'),
    url(r'^edit-my-information/$',views.myself_edit,name='edit_my_information'),
    url(r'^my-image/$',views.my_image,name='my_image'),
    url(r'^upload-image/$',views.upload_image,name='upload_image'),

]