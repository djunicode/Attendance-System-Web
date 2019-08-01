import csv
from Attendance.models import Teacher, Student, Div, Subject, AppUser
from Attendance.models import SubjectTeacher, StudentLecture, StudentDivision
from datetime import datetime, timedelta, date
import math
import os

current_year = date.today().year


def SAPDump(path, div_name, overwrite=False, reverse_names=False):
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
        div = Div.objects.create(semester=semester, calendar_year=date.today().year, division=division)

    with open(path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            name = row[2]
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
                names = name.lower().split(' ')
                names = [name.capitalize() for name in names]
                if reverse_names:
                    if len(names) > 2:
                        user.first_name = names[-1]
                        user.middle_name = " ".join(names[1:-1])
                        user.last_name = names[0]
                    elif len(name) == 2:
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
                    elif len(name) == 2:
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
