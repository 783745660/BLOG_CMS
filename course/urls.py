#coding=utf-8
__author__ = 'CoderSong'
__date__ = '2019/7/23 13:52'

from django.conf.urls import url
from django.views.generic import TemplateView
import views

#基于类的视图，不需要在views.py中书写视图函数

app_name = 'course'
urlpatterns = [
    # url(r'^about/$',TemplateView.as_view(template_name='course/about.html'),name='about'), #通过templlate_name指定模板,访问该url后就会返回一个模板页面
    url(r'about/$',views.AboutView.as_view(),name='about'),
    url(r'^courses-list/$',views.CourseListView.as_view(),name='courses_list'),
    url(r'^courses-manage/$',views.ManageCourseListView.as_view(),name='courses_manage'),
    url(r'^create-course/$',views.CreateCoureseView.as_view(),name='create_course'),
    url(r'^delete-course/(?P<pk>\d+)/$',views.DeleteCourseView.as_view(),name='delete_course'),
    url(r'^create-lesson/$',views.CreatedLessonView.as_view(),name='create_lesson'),
    url(r'lessons-list/(?P<course_id>\d+)/$',views.ListLessonView.as_view(),name='lessons_list'),
    url(r'lesson-detail/(?P<lesson_id>\d+)/$',views.DetailLessonView.as_view(),name='lesson_detail'),
]