from django.db import models
from django.contrib import auth
from django.contrib.auth.models import AbstractUser
import time
import datetime


class AppUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    middle_name = models.CharField(max_length=32, null=True, default=None)

    def getfullname(self):
        if self.middle_name:
            return self.first_name + " " + self.middle_name + " " + self.last_name
        else:
            return self.first_name + " " + self.last_name

    def __str__(self):
        return self.username


class Subject(models.Model):
    name = models.CharField(max_length=50)
    semester = models.PositiveSmallIntegerField()
    subjectCode = models.CharField(max_length=10)

    def __str__(self):
        return self.subjectCode + ": " + self.name


class Teacher(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, primary_key=True)
    specialization = models.CharField(max_length=50, null=True, blank=True)
    teacherID = models.CharField(max_length=20)
    subject = models.ManyToManyField(Subject, related_name='teacher', through='SubjectTeacher')

    def __str__(self):
        return self.user.getfullname()


class Div(models.Model):
    semester = models.PositiveSmallIntegerField()
    calendar_year = models.PositiveIntegerField(default=datetime.date.today().year)
    division = models.CharField(max_length=10)
    classteacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        yearname = ""
        semester = self.semester
        if semester <= 2:
            yearname = "FE"
        elif semester <= 4:
            yearname = "SE"
        elif semester <= 6:
            yearname = "TE"
        elif semester <= 8:
            yearname = "BE"
        return yearname + "_" + self.division

    def get_class_type(self):
        if len(self.division) == 1:
            return "Class"
        elif len(self.division) == 2 and self.division[1].isdigit():
            return "Practical"
        else:
            return "Elective"

    @staticmethod
    def yearnameToYear(yearname):
        if yearname == "FE":
            year = 1
        elif yearname == "SE":
            year = 2
        elif yearname == "TE":
            year = 3
        elif yearname == "BE":
            year = 4
        return year


class Lecture(models.Model):
    roomNumber = models.CharField(max_length=32, blank=True)
    startTime = models.TimeField(auto_now=False, auto_now_add=False)
    endTime = models.TimeField(auto_now=False, auto_now_add=False)
    date = models.DateField(auto_now=False, auto_now_add=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    div = models.ForeignKey(Div, on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    attendanceTaken = models.BooleanField(default=False)

    def __str__(self):
        return str(self.div) + " " + self.getTimeString()

    def getTimeString(self):
        return self.startTime.strftime("%H:%M:%S") + " - " + self.endTime.strftime("%H:%M:%S")

    def getDateTimeString(self):
        return self.date.strftime("%d-%m-%Y") + " : " + self.getTimeString()


class Student(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, primary_key=True)
    sapID = models.BigIntegerField(unique=True)
    div = models.ManyToManyField(Div, related_name='student', through='StudentDivision')
    lecture = models.ManyToManyField(Lecture, related_name='student', through='StudentLecture')

    def __str__(self):
        return self.user.getfullname()

    def getfullname(self):
        return self.user.getfullname()


class StudentLecture(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)


class SubjectTeacher(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    div = models.ForeignKey(Div, on_delete=models.CASCADE, null=True)


class StudentDivision(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    division = models.ForeignKey(Div, on_delete=models.CASCADE)
