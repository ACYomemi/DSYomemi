# -*- coding: gbk -*-
import json
import os.path
import random

from django.core.exceptions import *
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse

from Yomemi.models import *

'''
StudentInfo(StudentID, name, pwd, dept, totalScore, compulsoryScore, totalGPA, compulsoryGPA)
TeacherInfo(teacherID, name, pwd)
CourseInfo(courseID, name, score, teacherID, descript)
Compulsory(dept, course)
CourseSelect(studentID, courseID, grade)
Notice(ID, teacherID, text, timestamp)
'''
def login(request):
    # insertdata()
    if request.session.get('is_login'):
        return redirect('../index/')
    if request.method == 'GET':
        message = None
        if request.session.get('message'):
            message = request.session.get('message')
            request.session['message'] = None
        return render(request, 'login.html', {'message': message})
    if request.method == 'POST':
        ID = request.POST.get('user')
        pwd = int(request.POST.get('pwd'))
        role = request.POST.get('role')
        try:
            if role == 'STU':
                user = StudentInfo.objects.get(studentID=ID)
            else:
                user = TeacherInfo.objects.get(teacherID=ID)
            if pwd == user.pwd:
                request.session['is_login'] = True
                request.session['role'] = role
                request.session['ID'] = ID
                request.session.set_expiry(0)
                return redirect('../index/')
            else:
                return render(request, 'login.html', {'message': '用户名或密码错误'})
        except ObjectDoesNotExist:
            return render(request, 'login.html', {'message': '用户名或密码错误'})
        except Exception as e:
            print(repr(e))
            return render(request, 'login.html', {'message': '发生内部错误，请联系管理员'})


def timeline(request):
    return render(request, 'timeline.html')


def index(request):
    if not request.session.get('is_login'):
        request.session['message'] = '登录信息已失效，请重新登入'
        return redirect('../login/')
    if request.method == 'POST':
        if 'logout' in request.POST:
            request.session.flush()
            request.session['message'] = '登出成功，请重新登入'
            return redirect('../login')
    ID = request.session['ID']
    user = StudentInfo.objects.get(studentID=ID)
    course_list = CourseSelect.objects.filter(studentID=ID).values('courseID', 'courseID__courseName',
                                                                   'courseID__teacherID__teacherName',
                                                                   'courseID__descript', 'grade')
    return render(request, 'index.html',
                  {
                      'name': user.studentName,
                      'grades': [user.totalGPA, user.totalScore, user.compulsoryGPA, user.compulsoryScore],
                      'course_list': list(course_list)
                  })


def search(request, keyword=''):
    if not request.session.get('is_login'):
        request.session['message'] = '登录信息已失效，请重新登入'
        return redirect('../login/')
    if request.method == 'POST':
        select_list = request.POST.getlist('content[]')
        op = []
        for ID in select_list:
            try:
                CourseSelect.objects.create(studentID_id=request.session['ID'], courseID_id=ID)
                print(CourseSelect.objects.all())
            except Exception as ex:
                op.append(ID)
        dict = {'len': len(op), 'list': op}
        print(dict)
        return HttpResponse(json.dumps(dict), status=200)
    if request.method == 'GET':
        course_list = CourseInfo.objects.filter(
            models.Q(courseName__icontains=keyword) | models.Q(teacherID__teacherName__icontains=keyword)).values(
            'courseID', 'courseName',
            'score',
            'teacherID__teacherName')
        if not course_list.exists():
            course_list = [{'errmsg': '无查询结果'}]
        return render(request, 'test.html', {'course_list': list(course_list)})
    # Create your views here.
