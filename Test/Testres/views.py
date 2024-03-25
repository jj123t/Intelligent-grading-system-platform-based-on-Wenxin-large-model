import io

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import models
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt

from Testres import models
from Testres.models import (Student, TestPaper, Record, Evaluation)

from django.http import JsonResponse
from .forms import FileUploadForm
from .models import FileInfo
import os
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.core.files.storage import FileSystemStorage

@csrf_exempt
# Create your views here.
# 学生登录
def studentLogin(request):
    if request.method == 'POST':
        # 获取表单信息
        sid = request.POST.get('sid')
        password = request.POST.get('password')
        print("sid", sid, "password", password)
        # 通过学号获取该学生实体
        student = Student.objects.get(sid=sid)
        # student = Student.objects.get(sid=sid)
        print(student)
        if password == student.pwd:  # 登录成功
            request.session['username'] = sid  # user的值发送给session里的username
            request.session['is_login'] = True  # 认证为真
            # 查询考试信息
            paper = models.TestPaper.objects.filter(major=student.major)
            # 查询成绩信息
            grade = models.Record.objects.filter(sid=student.sid)

            # 渲染index模板
            return render(request, 'index.html', {'student': student, 'paper': paper, 'grade': grade})
        else:
            return render(request, 'login.html', {'message': '密码不正确'})
    elif request.method == 'GET':
        return render(request, 'login.html')
    else:
        return HttpResponse("请使用GET或POST请求数据")

# 首页
@csrf_exempt
def index(request):
    if request.session.get('is_login',None):  #若session认证为真
        username = request.session.get('username',None)
        print(username )
        student = Student.objects.get(sid=username)
        # 查询考试信息
        paper = models.TestPaper.objects.filter(major=student.major)
        return render(request, 'index.html',{'student': student,'paper': paper})
    else:
        return render(request, 'index.html')

@csrf_exempt
def userfile(request):
    if request.session.get('is_login',None):  #若session认证为真
        username = request.session.get('username',None)
        print(username )
        student = Student.objects.get(sid=username)
        # 查询考试信息
        paper = models.TestPaper.objects.filter(major=student.major)
        return render(request, 'userfile.html',{'student': student})

@csrf_exempt
def stuinfo(request):
    if request.session.get('is_login', None):
        username = request.session.get('username',None)
        print(username )
        student = Student.objects.get(sid=username)
        record = models.Record.objects.filter(sid=student.sid)
        evaluations = models.Evaluation.objects.filter(student=student)
        print(evaluations)
        context = {
            'student': student,
            'record': record,
            'evaluations': evaluations,
        }
        return render(request, 'showInfo.html',context)

#学生退出登录
@csrf_exempt
def stulogout(request):
    # logout(request)
    request.session.clear()
    # url = reverse('exam:index')
    return render(request, 'login.html')
    return redirect(url)

# 考试信息
@csrf_exempt
def startExam(request):
    sid = request.GET.get('sid')
    title = request.GET.get('title')  # 试卷名字 唯一
    subject1 = request.GET.get('subject')  # 考试科目
    # 获取学生信息
    student = Student.objects.get(sid=sid)
    # 试卷信息
    paper = TestPaper.objects.filter(title=title,course__course_name=subject1)
    context = {
        'student': student,
        'paper': paper,
        'title': title,
        'subject':subject1,
        'count': paper.count()   # 数据表中数据的条数
    }
    return render(request, 'exam.html', context=context)
@csrf_exempt
def examinfo(request):
    if request.session.get('is_login',None):  #若session认证为真
        username = request.session.get('username',None)
        student = Student.objects.get(sid=username)
        # 查询成绩信息
        grade = models.Record.objects.filter(sid=student.sid)
        return render(request, 'examinfo.html',{'student': student,'grade': grade})
    else:
        return render(request, 'examinfo.html')

@csrf_exempt
# 计算考试成绩
def calculateGrade(request):
    if request.method == 'POST':
        sid = request.POST.get('sid')
        subject1 = request.POST.get('subject')
        student = Student.objects.get(sid=sid)
        paper = models.TestPaper.objects.filter(major=student.major)
        grade = models.Record.objects.filter(sid=student.sid)
        course = models.Course.objects.filter(course_name=subject1).first()
        from django.utils.datetime_safe import datetime
        now = datetime.now()
        # 计算考试成绩
        questions = models.TestPaper.objects.filter(course__course_name=subject1). \
            values('pid').values('pid__id', 'pid__answer', 'pid__score')

        stu_grade = 0  # 初始化一个成绩
        for p in questions:
            qid = str(p['pid__id'])
            stu_ans = request.POST.get(qid)
            cor_ans = p['pid__answer']
            if stu_ans == cor_ans:
                stu_grade += p['pid__score']
        models.Record.objects.create(sid_id=sid, course_id=course.id, grade=stu_grade, rtime=now)
        context = {
            'student': student,
            'paper': paper,
            'grade': grade
        }
        return render(request, 'index.html', context=context)


from django.shortcuts import render
from .forms import ImageUploadForm
from .models import ImageUpload
import os
from paddleocr import PaddleOCR, draw_ocr
os.environ["KMP_DUPLICATE_LIB_OK"]= "TRUE"
import cv2
import numpy as np
import os
# from PIL import Image
import numpy as np
import io

def handleImage(image_file):
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    path = image_file.url[1::]
    print("path is : " + path)
    result = ocr.ocr(path, cls=True)
    print(result)
    # # 输出识别结果
    for line in result:
        print(line)
        x, y = line[-1]
        line_text = ' '.join(x)
        # print(line_text)
    from PIL import Image
    image = Image.open(path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[-1][0] for line in result]
    scores = [line[-1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='./doc/fonts/simfang.ttf')
    im_show = Image.fromarray(im_show)
    im_show.save(image_file.url[1::])
    # return im_show
    # im_show.show()

def show_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_upload = form.save()
            handleImage(image_upload.image)
            # 返回新上传的图片信息
            response_data = {
                'id': image_upload.id,
                'image_url': image_upload.image.url,
            }
            return JsonResponse(response_data)
    else:
        form = ImageUploadForm()
    return render(request, 'upload_form.html', {'form': form})

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'upload_success.html')
    else:
        form = ImageUploadForm()
    return render(request, 'upload_form.html', {'form': form})


from django.http import JsonResponse

def image_gallery(request):
    images = ImageUpload.objects.all()
    return render(request, 'image_gallery.html', {'images': images})



from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest


@csrf_exempt
def submit_evaluation(request):
    if request.method == 'POST':
        username = ""
        if request.session.get('is_login', None):  # 若session认证为真
            username = request.session.get('username', None)
        student = Student.objects.get(sid=username)
        subject = request.POST.get('subject')
        evaluator_type = request.POST.get('evaluator_type')
        comment = request.POST.get('comment')
        print(student)
        print(evaluator_type)
        print(subject)
        print(comment)
        if (evaluator_type == "1"):
            evaluator_type = Evaluation.STUDENT_EVALUATION
        else:
            evaluator_type = Evaluation.TEACHER_EVALUATION
        # 验证数据是否有效
        if not subject or not evaluator_type or not comment:
            print("eroor and not zd")
            return HttpResponseBadRequest('缺少必要字段')
        # 创建Evaluation对象并保存到数据库
        evaluation = Evaluation(
            student=student,
            subject=subject,
            evaluator_type=evaluator_type,
            comment=comment,
        )
        evaluation.save()

        # 返回JSON响应或重定向到成功页面
        messages.success(request, '评价已提交')
        return redirect('index/')  # 替换为你的成功页面URL

    # 如果不是POST请求，则返回表单页面
    return render(request, 'showInfo.html')


