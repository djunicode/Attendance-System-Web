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
                else:
                    student = Student.objects.get(user=user)

                StudentDivision.objects.get_or_create(student=student, division=div)

                print(student)
    csvFile.close()


def WorkLoadDump(path, semester=current_sem):
    with open(path, 'r', encoding='utf-8-sig') as csvFile:
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
                all_divs = Div.objects.filter(semester=sem, calendar_year=current_year)
                divs = all_divs.filter(division__in=div_names)
                users = []
                for name in teacher_names:
                    try:
                        users.append(AppUser.objects.get(first_name=name[0]+ " " +name[-1]))
                    except AppUser.DoesNotExist:
                        print("\033[91m{}\033[00m" .format(name[0] + " " + name[1] + " not found"))

                teachers = Teacher.objects.filter(user__in=users)
                for teacher in teachers:
                    for div in divs:
                        if not all_divs.filter(division=div.division + sub).exists():
                            SubjectTeacher.objects.get_or_create(subject=subject, div=div, teacher=teacher)
                            print(subject, div, teacher)
                        else:
                            elective_div = all_divs.get(division=div.division + sub)
                            SubjectTeacher.objects.get_or_create(subject=subject, div=elective_div, teacher=teacher)
                            print(subject, elective_div, teacher)


def createTeacher(id, f_name, l_name, spec="Computer Engineering"):
    user = AppUser.objects.create(username=id, password="pass@123")
    user.set_password('pass@123')
    user.first_name = f_name
    user.last_name = l_name
    user.is_teacher = True
    user.save()
    teacher = Teacher.objects.create(user=user, teacherID=id, specialization=spec)
    print(teacher)


def fillPracs(div_name, end1, end2, end3):
    yearname, division = div_name.split("_")
    year = Div.yearnameToYear(yearname)

    if date.today().month < 6:
        semester = year * 2
    elif date.today().month > 6:
        semester = year * 2 - 1

    div = Div.objects.get(semester=semester, calendar_year=date.today().year, division=division)
    p1, _ = Div.objects.get_or_create(semester=semester, calendar_year=date.today().year, classteacher=div.classteacher,
                                      division=division + "1")
    p2, _ = Div.objects.get_or_create(semester=semester, calendar_year=date.today().year, classteacher=div.classteacher,
                                      division=division + "2")
    p3, _ = Div.objects.get_or_create(semester=semester, calendar_year=date.today().year, classteacher=div.classteacher,
                                      division=division + "3")
    p4, _ = Div.objects.get_or_create(semester=semester, calendar_year=date.today().year, classteacher=div.classteacher,
                                      division=division + "4")

    students = Student.objects.filter(div=div)
    for student in students:
        if student.sapID <= end1:
            print(StudentDivision.objects.get_or_create(student=student, division=p1)[0])
        elif student.sapID <= end2:
            print(StudentDivision.objects.get_or_create(student=student, division=p2)[0])
        elif student.sapID <= end3:
            print(StudentDivision.objects.get_or_create(student=student, division=p3)[0])
        else:
            print(StudentDivision.objects.get_or_create(student=student, division=p4)[0])


def fillPracs2(path, div_name, new_div_name):
    yearname, division = div_name.split("_")
    year = Div.yearnameToYear(yearname)

    if date.today().month < 6:
        semester = year * 2
    elif date.today().month > 6:
        semester = year * 2 - 1

    div = Div.objects.get(semester=semester, calendar_year=date.today().year, division=division)
    p1, _ = Div.objects.get_or_create(semester=semester, calendar_year=date.today().year, classteacher=div.classteacher,
                                      division=new_div_name)

    with open(path, 'r', encoding='utf-8-sig') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if row[0] != '':
                sap = row[0]
                # print(sap)
                try:
                    student = Student.objects.get(sapID=sap)
                    StudentDivision.objects.get_or_create(student=student, division=p1)
                    print(student.user.first_name, student.user.last_name, student.sapID)
                except:
                    print("\033[91m{}\033[00m" .format(sap + " not found"))
                


def TeacherDump(path, spec="Computer Engineering"):
    with open(path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if row[0] != '':
                id = row[0]
                f_name = row[1]
                user = AppUser.objects.create(username=id, password="pass@123")
                user.set_password('pass@123')
                user.first_name = f_name
                user.is_teacher = True
                user.save()
                teacher = Teacher.objects.create(user=user, teacherID=id, specialization=spec)
                print(teacher)

# TO RUN THIS SCRIPT -
#
# python manage.py shell
#
# from SAP import dump
#
# AVAILABLE FUNCTIONS USAGE EXAMPLES -
# reads names in format "FirstName MiddleName LastName", classteacher is left Null and doesn't overwrite old entries
# dump.SAPDump("SAP/TEA.csv", "TE_A")
#
# reads names in format "LastName FirstName MiddleName", classteacher is Sindhu Nair and will overwrite old
# conflicting entries
# dump.SAPDump("SAP/TEA.csv", "TE_A", overwrite=True, reverse_names=True, classteacher="Sindhu Nair")
# 
# dump teachers data
# dump.TeacherDump("SAP/Teachers.csv")
#
# populates current semester (odd for june to dec and even for jan to may) with teacher workload data
# dump.WorkLoadDump("SAP/WorkLoad.csv")
#
# creates a teacher with id and username 19210161, first name Pranit and last name Bari
# dump.createTeacher(19210161, "Pranit", "Bari")
#
# creates 4 practical batches, "TE_A1" upto 20, "TE_A2" upto 41, "TE_A3" upto 59 and "TE_A4" for remaining
# dump.fillPracs("TE_A", 60004170020, 60004170041, 60004170059)
# 
# For pracs batches (TE and BE)
# dump.fillPracs2("SAP/TE_A1","TE_A","A1")
