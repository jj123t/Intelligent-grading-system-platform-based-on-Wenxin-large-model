"""exam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path as url
from Testres import views
from django.conf.urls.static import static
from django.conf import settings
# app_name = ‘exam’
urlpatterns = ([
    path('admin/', admin.site.urls),
    url(r'^$', views.index),  # 默认访问首页
    url('index/', views.index, name='index'),
    url('studentLogin/', views.studentLogin, name='studentLogin'),  # 学生登录
    url('startExam/', views.startExam, name='startExam'),  # 开始考试
    url('calculateGrade/', views.calculateGrade, name='calculateGrade'),  # 考试评分
    path('stulogout/', views.stulogout, name='stulogout'),  # 学生退出登录
    path('userfile/', views.userfile, name='userfile'),  # 个人信息
    path('examinfo/', views.examinfo, name='examinfo'),  # 考试信息
    # path('upload/', views.upload_image, name='upload_image'),
    path('upload/', views.show_image, name='upload_image'),
    path('gallery/', views.image_gallery, name='image_gallery'),
    path('info/', views.stuinfo, name='show_info'),
    path('info/submitview/', views.submit_evaluation, name='submit_evaluation'),
])

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
