#coding=utf-8

from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,ListView  #使用ListView从数据表中读取数据库中的数据
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from braces.views import LoginRequiredMixin


from .models import Course,Lesson
from .forms import CreateCourseForm,CreateLessonForm


# Create your views here.

class AboutView(TemplateView):
    template_name = 'course/about.html'


class CourseListView(ListView):
    '''
    继承ListView类，从数据表course_course中获取course数据，并定义要传入模板的变量为courses和模板文件course/course_list.html
    '''
    model = Course
    context_object_name = 'courses'
    template_name = 'course/course_list.html'


class UserMixin(object):
    '''
    编写一个要被继承的Mixin类
    '''
    def get_queryset(self):
        qs = super(UserMixin,self).get_queryset()
        return qs.filter(user=self.request.user)


class UserCourseMixin(UserMixin,LoginRequiredMixin):
    '''
    继承UserMixin和LoginRequiredMixin类
    '''
    model = Course
    login_url = '/account/login/'


class ManageCourseListView(UserCourseMixin,ListView):
    '''
    实现用户管理课程的视图类,从当前登录用户的course_course数据表中获取所有课程，模板变量为courses
    要传递给的模板为template_name
    '''
    context_object_name = 'courses'
    template_name = 'course/manage/manage_course_list.html'



class CreateCoureseView(UserCourseMixin,CreateView):
    '''
    继承UserCourseMixin,让用户在登录的状态下获取自己的course_course数据表
    继承CreateView是处理用户以GET方法访问时，直接在页面中显示表单，不用在写get()方法
    '''
    fields = ['title','overview']
    template_name = 'course/manage/create_course.html'

    def post(self, request, *args, **kwargs):
        '''
        处理用户以post方法访问，如果表单填写无误将页面重定向到/course/courses_manege
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        form = CreateCourseForm(data=request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.user = self.request.user
            new_course.save()
            return redirect('course:courses_manage')
            #return redirect('/course/courses-manege/') #这里的redirect很厉害还可以传递url
        return self.render_to_response({"form":form})



class DeleteCourseView(UserCourseMixin,DeleteView):
    '''
    定义用户删除课程类视图
    '''
    template_name = 'course/manage/delete_course_confirm.html'
    success_url = reverse_lazy('course:courses_manage')




class CreatedLessonView(LoginRequiredMixin,View):
    '''
    定义发布课程内容类视图，由于这里继承的是View，需要重写get()和post()方法
    '''
    model = Lesson
    login_url = '/account/login/'

    def get(self,request,*args,**kwargs):
        form = CreateLessonForm(user=self.request.user) #初始化方法在该项目中已被改写
        return render(request,'course/manage/create_lesson.html',{"form":form})

    def post(self,requst,*args,**kwargs):
        form = CreateLessonForm(self.request.user,requst.POST,requst.FILES)
        if form.is_valid():
            new_lesson = form.save(commit=False)
            new_lesson.user = self.request.user
            new_lesson.save()
            return redirect('course:courses_manage')


class ListLessonView(LoginRequiredMixin,TemplateResponseMixin,View):

    login_url = '/account/login/'
    template_name = 'course/manage/list_lessons.html'

    def get(self,request,course_id):
        '''
        得到每一个course下的内容列表
        :param request:
        :param course_id:
        :return:
        '''
        course = get_object_or_404(Course,id=course_id)
        return self.render_to_response({'course':course}) #在前端中利用course.lesson得到该课程的所有lesson


class DetailLessonView(LoginRequiredMixin,TemplateResponseMixin,View):
    login_url = '/account/login/'
    template_name = 'course/manage/detail_lesson.html'

    def get(self,request,lesson_id):
        '''
        查看每一个course下的每一个lesson内容
        :param request:
        :param lesson_id:
        :return:
        '''
        lesson = get_object_or_404(Lesson,id=lesson_id)
        return self.render_to_response({'lesson':lesson}) #在前端中利用course.lesson得到该课程的所有lesson






