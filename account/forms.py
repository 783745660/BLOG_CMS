#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/7/18 15:21'

from django import forms
from django.contrib.auth.models import User

from .models import UserProfile,UserInfo


class LoginForm(forms.Form):
    '''
    django.forms.Form的子类，提供用户登录的表单类，由于本站使用内置登录方法，故不需要自定义登录表单,该类可直接被注释掉
    '''
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterationForm(forms.ModelForm):
    '''
    一般要改写数据库记录是会选择继承ModelForm,仅提交表单的话就继承Form
    '''
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)

    class Meta:
        '''
        内部类,即表明向User数据表中写入username,email
        '''
        model = User
        fields = ('username','email')

    def clean_password2(self):
        '''
        检验输入密码,该方法在调用实例表单对象的is_valid()方法时被执行
        :return:
        '''
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('passwords do not match.')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone','birth')


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('school','company','profession','address','aboutme','image')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

