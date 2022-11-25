# -*- coding: gbk -*-
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from Yomemi.uselib import *


# Create your models here.


class StudentInfo(models.Model):
    studentID = models.CharField(primary_key=True, max_length=13)  # ѧ����
    studentName = models.CharField(max_length=10)  # ����
    pwd = models.DecimalField(max_digits=6, decimal_places=0)  # ����Ĺ�ϣֵ
    dept = models.CharField(max_length=2)  # ����Ժϵ������CS
    totalScore = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    compulsoryScore = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    totalGPA = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    compulsoryGPA = models.DecimalField(max_digits=3, decimal_places=2, default=0)


class TeacherInfo(models.Model):
    teacherID = models.CharField(primary_key=True, max_length=13)  # ѧ����
    teacherName = models.CharField(max_length=10)  # ����
    pwd = models.DecimalField(max_digits=6, decimal_places=0)  # ����Ĺ�ϣֵ


class CourseInfo(models.Model):
    courseID = models.CharField(primary_key=True, max_length=12)  # �γ̺ţ�12λ��
    courseName = models.CharField(max_length=20)  # �γ���
    score = models.DecimalField(max_digits=2, decimal_places=0)  # ѧ�֣���0-10֮��
    teacherID = models.ForeignKey('TeacherInfo', related_name='teacherID_CourseInfo',
                                  on_delete=models.CASCADE)  # ���ν�ʦ��ţ�ӳ�䵽�û����е������ֶΣ���������ɾ��
    descript = models.TextField(null=True, blank=True)  # �γ���������������

    class Meta:
        constraints = \
            [
                models.CheckConstraint(check=models.Q(score__gte=0) & models.Q(score__lte=10),
                                       name='CourseInfoScore')
            ]


class Compulsory(models.Model):
    dept = models.CharField(max_length=2)
    course = models.CharField(max_length=9)


class CourseSelect(models.Model):
    studentID = models.ForeignKey('StudentInfo', related_name='studentID_CourseSelect',
                                  on_delete=models.CASCADE)  # ѡ�ε�ѧ�ţ�ӳ�䵽�û����е�ѧ�����ֶΣ���������ɾ��
    courseID = models.ForeignKey('CourseInfo', related_name='courseID_CourseSelect',
                                 on_delete=models.CASCADE)  # ѡ�εĿκţ�ӳ�䵽�γ̱��еĿκ��ֶΣ���������ɾ��
    grade = models.DecimalField(max_digits=3, decimal_places=0, null=True, blank=True)  # ������0��100֮�䣬����һλС������������
    class Meta:
        unique_together = ('studentID', 'courseID')
        constraints = \
            [
                models.CheckConstraint(check=models.Q(grade=None) | models.Q(grade__gte=0) & models.Q(grade__lte=100),
                                       name='CourseSelectGrade')
            ]


@receiver(post_save, sender=CourseSelect)
def post_save_CourseSelect(sender, instance, created, **kwargs):
    if instance.grade is not None and instance.grade >= 60:
        target = instance.studentID
        score = instance.courseID.score
        target.totalGPA = (target.totalGPA * target.totalScore + score * GPA(instance.grade)) / (
                target.totalScore + score)
        target.totalScore = target.totalScore + score
        if Compulsory.objects.filter(dept=target.dept, course=instance.courseID.courseID[0:9]).exists():
            target.compulsoryGPA = (target.compulsoryGPA * target.compulsoryScore + score * GPA(instance.grade)) / (
                    target.compulsoryScore + score)
            target.compulsoryScore = target.compulsoryScore + score
        target.save()
    return


@receiver(pre_delete, sender=CourseSelect)
def pre_delete_CourseSelect(sender, instance, **kwargs):
    if instance.grade is not None and instance.grade >= 60:
        target = instance.studentID
        score = instance.courseID.score
        if target.totalScore - score > 0:
            target.totalGPA = (target.totalGPA * target.totalScore - score * GPA(instance.grade)) / (
                    target.totalScore - score)
        else:
            target.totalGPA = 0
        target.totalScore = target.totalScore - score
        if Compulsory.objects.filter(dept=target.dept, course=instance.courseID.courseID[0:9]).exists():
            if target.compulsoryScore - score > 0:
                target.compulsoryGPA = (target.compulsoryGPA * target.compulsoryScore - score * GPA(instance.grade)) / (
                        target.compulsoryScore - score)
            else:
                target.compulsoryGPA = 0
            target.compulsoryScore = target.compulsoryScore - score
        target.save()
    return


class Notice(models.Model):
    ID = models.AutoField(primary_key=True)
    teacherID = models.ForeignKey('TeacherInfo', related_name='studentID_Notice', on_delete=models.CASCADE)
    title = models.CharField(max_length=15, default='Notice')
    text = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
