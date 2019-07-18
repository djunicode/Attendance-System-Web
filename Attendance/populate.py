from .models import (Student, AppUser, Teacher, Lecture, Div, Subject,
                     StudentLecture, SubjectTeacher, DivisionSubject, StudentDivision, DivisionTeacher)
import random
from datetime import datetime, timedelta, date
import math
from faker import Faker


def fillStudent(count=50):
    fake = Faker()
    for year in range(1, 5):
        for sapcnt in range(1, 2 + int(count / 4)):
            sap = 60004000000 + (19 - year) * 10000 + sapcnt
            user = AppUser.objects.create(username=sap, password='pass@123')
            user.set_password('pass@123')
            user.is_student = True
            name = fake.name().split()
            user.first_name = name[0]
            user.last_name = name[1]
            user.save()
            u = Student.objects.create(user=user, sapID=sap)
            u.save()


def fillTeacher(count=15):
    fake = Faker()
    for sap in range(90000000001, 90000000002 + count):
        user = AppUser.objects.create(username=sap, password='pass@123')
        user.set_password('pass@123')
        user.is_teacher = True
        name = fake.name().split()
        user.first_name = name[0]
        user.last_name = name[1]
        user.save()
        u = Teacher.objects.create(user=user, teacherID=sap, specialization="Computer Stuff")
        u.save()


def fillSubject():
    Subject.objects.create(name="SPA", semester=2, subjectCode="FEC205")
    Subject.objects.create(name="DS", semester=3, subjectCode="FEC305")
    Subject.objects.create(name="OOPM", semester=3, subjectCode="FEC306")
    Subject.objects.create(name="COA", semester=4, subjectCode="FEC402")
    Subject.objects.create(name="AP2", semester=2, subjectCode="FEC202")
    Subject.objects.create(name="OS", semester=4, subjectCode="FEC404")
    Subject.objects.create(name="ML", semester=5, subjectCode="FEC501")
    Subject.objects.create(name="BCF", semester=5, subjectCode="FEC503")
    Subject.objects.create(name="ED", semester=2, subjectCode="FEC206")


def fillDiv():
    teachers = list(Teacher.objects.all())
    for sem in range(1, 9):
        if len(teachers):
            teacher1 = random.choice(teachers)
            teachers.remove(teacher1)
        else:
            teacher1 = None
        if len(teachers):
            teacher2 = random.choice(teachers)
            teachers.remove(teacher2)
        else:
            teacher2 = None
        current_year = date.today().year
        Div.objects.create(semester=sem, division='A', classteacher=teacher1, calendar_year=current_year)
        Div.objects.create(semester=sem, division='B', classteacher=teacher2, calendar_year=current_year)
        for b in range(1, 5):
            Div.objects.create(semester=sem, division='A' + str(b), calendar_year=current_year,
                               classteacher=teacher1)
            Div.objects.create(semester=sem, division='B' + str(b), calendar_year=current_year,
                               classteacher=teacher2)


def fillLecture(count=50):
    if not (len(Div.objects.all()) and len(Subject.objects.all()) and len(Teacher.objects.all())):
        raise Exception('Need a division and subject to create lectures!')
    fake = Faker()
    for i in range(count):
        lecture = Lecture()
        lecture.roomNumber = random.choice(['C', 'L']) + random.choice(['1', '2', '3'])
        lecture.date = fake.date_this_year(before_today=True, after_today=False)
        lecture.startTime = fake.time_object(end_datetime=None)
        lecture.endTime = fake.time_object(end_datetime=None)
        lecture.div = random.choice(list(Div.objects.all()))
        lecture.subject = random.choice(list(Subject.objects.all()))
        lecture.teacher = random.choice(list(Teacher.objects.all()))
        lecture.save()

        SubjectTeacher.objects.get_or_create(subject=lecture.subject, teacher=lecture.teacher, div=lecture.div)
        DivisionTeacher.objects.get_or_create(division=lecture.div, teacher=lecture.teacher)
        DivisionSubject.objects.get_or_create(division=lecture.div, subject=lecture.subject)


def fillAll():
    fillStudent()
    fillTeacher()
    fillSubject()
    fillDiv()
    fillLecture()

    students = Student.objects.all()
    for student in students:
        sap_data = student.sapID % 60004000000
        sap_no = sap_data % 1000
        year = 19 - (sap_data - sap_no) / 10000
        divisions = Div.objects.filter(year=year)
        div_alpha = random.choice(['A', 'B'])
        div = div_alpha + random.choice(['1', '2', '3', '4'])
        full_div = divisions.filter(division=div_alpha)
        for fd in full_div:  # iterate over queryset with 2 sems
            StudentDivision.objects.create(student=student, division=fd)
        prac_div = divisions.filter(division=div)
        for d in prac_div:
            StudentDivision.objects.create(student=student, division=d)

    divisions = Div.objects.all()
    weighted_random = [True] * 9 + [False] * 1

    for div in divisions:
        studentdiv = StudentDivision.objects.filter(division=div)
        lectures = Lecture.objects.filter(div=div)
        for sd in studentdiv:
            for lec in lectures:
                attended = random.choice(weighted_random)
                if attended:
                    StudentLecture.objects.create(student=sd.student, lecture=lec)


# TO RUN THIS SCRIPT -
#
# python manage.py shell
#
# from Attendance import populate
#
# populate.fillAll()
# please follow the above order and make sure you dont have your own users with real SAP IDs
# just have a superuser and then run the above commands
