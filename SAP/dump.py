import csv
from Attendance.models import Teacher, Student, Div, Subject, AppUser
from Attendance.models import SubjectTeacher, StudentLecture, StudentDivision
from datetime import datetime, timedelta, date
import math
import os

current_year = date.today().year

if date.today().month < 6:
    current_sem = "even"
else:
    current_sem = "odd"


def SAPDump(path, div_name, overwrite=False, reverse_names=False, classteacher=None):
    yearname, division = div_name.split("_")
    year = Div.yearnameToYear(yearname)

    if date.today().month < 6:
        semester = year * 2
    elif date.today().month > 6:
        semester = year * 2 - 1

    div_exists = Div.objects.filter(semester=semester, calendar_year=date.today().year, division=division).exists()
    if div_exists and not overwrite:
        raise Exception("Div already exists, set overwrite to True to overwrite")
    elif div_exists:
        div = Div.objects.get(semester=semester, calendar_year=date.today().year, division=division)
    else:
        if classteacher:
            names = classteacher.strip().split(' ')
            teacher = Teacher.objects.get(user=AppUser.objects.get(first_name=names[0], last_name=names[1]))
            div = Div.objects.create(semester=semester, calendar_year=date.today().year, division=division)
            div.classteacher = teacher
            div.save()
        else:
            div = Div.objects.create(semester=semester, calendar_year=date.today().year, division=division)

    with open(path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if len(row[1]) and len(row[2]):
                name = row[2].lower()
                sap = int(row[1])
                try:
                    user = AppUser.objects.get(username=sap)
                    found = True
                except AppUser.DoesNotExist:
                    user = AppUser.objects.create(username=sap, password='pass@123')
                    user.set_password('pass@123')
                    user.is_student = True
                    found = False

                if (not found) or overwrite:
                    names = name.split(' ')
                    names = [name.capitalize() for name in names]
                    if reverse_names:
                        if len(names) > 2:
                            user.first_name = names[1]
                            user.middle_name = " ".join(names[2:])
                            user.last_name = names[0]
                        elif len(names) == 2:
                            user.first_name = names[1]
                            user.last_name = names[0]
                        else:
                            user.first_name = name
                            user.last_name = ""
                    else:
                        if len(names) > 2:
                            user.first_name = names[0]
                            user.middle_name = " ".join(names[1:-1])
                            user.last_name = names[-1]
                        elif len(names) == 2:
                            user.first_name = names[0]
                            user.last_name = names[1]
                        else:
                            user.first_name = name
                            user.last_name = ""

                    user.save()

                if not found:
                    student = Student.objects.create(user=user, sapID=sap)
                    StudentDivision.objects.create(student=student, division=div)

                print(Student.objects.get(user=user))
    csvFile.close()


def WorkLoadDump(path, semester=current_sem):
    with open(path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        yr = ''
        sub = ''
        for row in reader:
            if row[0] != '':
                yr = row[0]
            if row[1] != '':
                sub = row[1]
            if row[2] != '' and row[3] != '':
                div_names = row[2].split('&')
                teacher_names = [name.strip().split(' ') for name in row[3].split('/')]
                year = Div.yearnameToYear(yr.upper())
                if semester == "even":
                    sem = year * 2
                else:
                    sem = year * 2 - 1
                subject, _ = Subject.objects.get_or_create(name=sub, semester=sem)
                divs = Div.objects.filter(
                    division__in=div_names,
                    semester=sem,
                    calendar_year=current_year
                )
                users = []
                for name in teacher_names:
                    try:
                        users.append(AppUser.objects.get(first_name=name[0], last_name=name[-1]))
                    except AppUser.DoesNotExist:
                        print(name[0] + " " + name[1] + " not found")

                teachers = Teacher.objects.filter(user__in=users)
                for teacher in teachers:
                    for div in divs:
                        SubjectTeacher.objects.get_or_create(subject=subject, div=div, teacher=teacher)
                        print(subject, div, teacher)


def createTeacher(id, f_name, l_name, spec="Computer Engineering"):
    user = AppUser.objects.create(username=id, password="pass@123")
    user.set_password('pass@123')
    user.first_name = f_name
    user.last_name = l_name
    user.is_teacher = True
    user.save()
    teacher = Teacher.objects.create(user=user, teacherID=id, specialization=spec)
    print(teacher)
