#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/7/23 15:13'

from django import forms
from .models import Course,Lesson

class CreateCourseForm(forms.ModelForm):
    '''
    定义创建course表单
    '''
    class Meta:
        model = Course
        fields = ('title','overview')



class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['course', 'title', 'video', 'description', 'attach']
    def __init__(self, user, *args, **kwargs):
        '''
          该方法的作用是，因此前一个用户已经创建了很多课程course，我们的lesson外键时course,因此，这里会把数据库中的所有course都展示出来，
          故重写__init__()初始化方法，使该表单只显示当前用户创建的课程course
          :param user:
          :param args:
          :param kwargs:
          '''
        super(CreateLessonForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(user=user)