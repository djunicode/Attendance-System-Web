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

    def getname(self):
        return self.first_name + " " + self.last_name


class Subject(models.Model):
    name = models.CharField(max_length=50)
    semester = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name + '(sem ' + str(self.semester) + ')'


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
    classteacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, default=None)

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

    def semester_order(self):
        if datetime.date.today().month < 6:
            if self.semester % 2 == 0:
                return 1
            else:
                return 0
        else:
            if self.semester % 2 == 0:
                return 0
            else:
                return 1

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
        return str(self.div) + " " + self.subject.name + " " + self.getShortTimeString()

    def getTimeString(self):
        return self.startTime.strftime("%H:%M:%S") + " - " + self.endTime.strftime("%H:%M:%S")

    def getShortTimeString(self):
        return self.startTime.strftime("%-I:%M") + "-" + self.endTime.strftime("%-I:%M")

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
    # Saves Attendance of a student
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.student) + " " + str(self.lecture)


class SubjectTeacher(models.Model):
    # Ternary relationship that stores which teacher teaches what to which div
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    div = models.ForeignKey(Div, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.teacher) + " " + str(self.subject) + " " + str(self.div)


class StudentDivision(models.Model):
    # So that students can be a part of a class, division or practical batch
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    division = models.ForeignKey(Div, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.student) + " " + str(self.division)
