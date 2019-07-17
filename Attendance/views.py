from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from . import forms
from django.views.generic import TemplateView
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
import json
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from rest_framework import generics, status
from .models import Teacher, Student, Lecture, Div, Subject, TimeTableLecture
from .models import SubjectTeacher, AppUser, StudentLecture, StudentDivision
from .serializers import (TeacherSerializer, StudentSerializer, LectureSerializer, DivSerializer, SubjectSerializer,
                          TimeTableLectureSerializer)
from rest_framework.authentication import TokenAuthentication
import datetime
import time
import csv


class HomePage(TemplateView):
    template_name = 'Attendance/index.html'


class ThanksPage(TemplateView):
    template_name = 'Attendance/logout_success.html'


def login_user_teacher(request):
    # logout(request)
    # username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('Attendance:dash')
    return render(request, 'Attendance/login.html', context={'form': forms.TeacherLoginForm()})


@login_required
def dash(request):
    return render(request, 'Attendance/login_success.html')


def signup(request):
    if request.method == 'POST':
        form = forms.UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('Attendance:dash')
    else:
        form = forms.UserCreateForm()
    return render(request, 'Attendance/signup.html', {'form': form})


# REST FRAMEWORK RELATED API VIEWS


class TeacherListView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TeacherSerializer

    def get_queryset(self):
        return Teacher.objects.all().filter(username=self.request.user)


class StudentListView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Student.objects.all().filter(username=self.request.user)


class LectureListView(generics.ListCreateAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LectureDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LectureSerializer

    def get_queryset(self):
        return Lecture.objects.all().filter(user=self.request.user)


class SubjectListView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        return Subject.objects.all().filter(user=self.request.user)


class DivisionListView(generics.ListCreateAPIView):
    queryset = Div.objects.all()
    serializer_class = DivSerializer


class DivisionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DivSerializer

    def get_queryset(self):
        return Div.objects.all().filter(user=self.request.user)


class TeachersSubjectDataView(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        teacherId = kwargs['teacherId']

        try:
            teacher = Teacher.objects.get(teacherID=teacherId)
        except Exception as e:
            response_data = {'error_message': "Invalid TeacherId" + str(e)}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        divisions = Div.objects.filter(classteacher=teacher, calendar_year=datetime.date.today().year)
        class_subjects = []
        for div in divisions:
            class_subjects_ordereddict = Subject.objects.filter(division=div).distinct()
            for subject in class_subjects_ordereddict:
                subject_json = SubjectSerializer(subject).data
                subject_json["div"] = str(div)
                class_subjects.append(subject_json)

        taught_subjects = []

        subjectteacher = SubjectTeacher.objects.filter(teacher=teacher)
        for st in subjectteacher:
            subject_json = SubjectSerializer(st.subject).data
            subject_json["div"] = str(st.div)
            taught_subjects.append(subject_json)

        division = None
        for div in divisions:
            if div.get_class_type() == "Class":
                division = div

        response_data = {
            'taught_subjects': taught_subjects,
            'class_subjects': class_subjects,
            'division_they_are_class_teacher_of': DivSerializer(division).data,
        }

        return JsonResponse(response_data, status=status.HTTP_200_OK)


class LoginTeacherView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):

        try:
            form_data = json.loads(request.body.decode())
            teacherId = form_data['teacherId']
            password = form_data['password']
        except Exception:
            teacherId = request.POST.get('teacherId')
            password = request.POST.get('password')

        teacher = Teacher.objects.get(teacherID=teacherId)
        user = authenticate(username=teacher.user.username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            login(request, user)

            response_data = {
                'token': token.key,
            }

            return JsonResponse(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {'error_message': "Cannot log you in"}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)


class LogoutTeacherView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        logout(request)
        response_data = {'success_message': 'Successfully logged you out'}
        return JsonResponse(response_data, status=status.HTTP_200_OK)


class SignUpTeacherView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):

        try:
            form_data = json.loads(request.body.decode())
            teacherId = form_data['teacherId']
            password = form_data['password']
            f_name = form_data['fname']
            l_name = form_data['lname']
            specialization = form_data['spec']
        except Exception:
            teacherId = request.POST.get('teacherId')
            password = request.POST.get('password')
            f_name = request.POST.get('fname')
            l_name = request.POST.get('lname')
            specialization = request.POST.get('spec')

        try:
            user = AppUser.objects.create(username=teacherId, password=password)
            user.first_name = f_name
            user.last_name = l_name
            user.set_password(password)
            user.is_teacher = True
            user.save()
            teacher = Teacher.objects.create(user=user, teacherID=teacherId, specialization=specialization)
            teacher.save()

            login(request, user)

            token, _ = Token.objects.get_or_create(user=user)

            response_data = {
                'token': token.key,
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {'error_message': "Cannot sign you up due to " + str(e)}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)


class GenericLoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):

        try:
            form_data = json.loads(request.body.decode())
            user_id = form_data['id']
            password = form_data['password']
        except Exception:
            user_id = request.POST.get('id')
            password = request.POST.get('password')

        user = authenticate(username=user_id, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            login(request, user)

            response_data = {
                'isStudent': user.is_student,
                'isTeacher': user.is_teacher,
                'token': token.key,
            }

            if user.is_student:
                response_data['user'] = StudentSerializer(Student.objects.get(user=user)).data
            else:
                response_data['user'] = TeacherSerializer(Teacher.objects.get(user=user)).data

            return JsonResponse(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {'error_message': "Cannot log you in"}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)


class GetAttendanceOfDay(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        subject_name = kwargs['subject']
        div = kwargs['div']
        try:
            date = kwargs['date']
            d, m, y = date.split('-')
            date = datetime.datetime(int(y), int(m), int(d)).date()
        except KeyError:
            date = datetime.date.today()

        yearname, division = div.split("_")
        year = Div.yearnameToYear(yearname)
        if date.month < 6:
            semester = year * 2
        else:
            semester = year * 2 - 1
        try:
            subject = Subject.objects.get(name=subject_name)
            div = Div.objects.get(division=division, semester=semester, calendar_year=datetime.date.today().year)

        except Subject.DoesNotExist:
            response_data = {'error_message': "Subject " + subject_name + " Does Not Exist"}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Div.DoesNotExist:
            response_data = {'error_message': "Division " + div + " Does Not Exist"}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        teacher = Teacher.objects.get(user=request.user)

        if div.classteacher is teacher:
            lecs = Lecture.objects.filter(date=date, div=div, subject=subject)
        else:
            lecs = Lecture.objects.filter(date=date, teacher=teacher, div=div, subject=subject)

        attendance_list = {}

        for lec in lecs:
            lecTime = lec.getTimeString()
            attendance_list[lecTime] = []
            student_lecs = StudentLecture.objects.filter(lecture=lec)
            present_students = [sl.student for sl in student_lecs]

            student_divs = StudentDivision.objects.filter(division=div)
            div_students = [sd.student for sd in student_divs]

            absent_students = list(set(div_students) - set(present_students))

            for student in present_students:
                student_json = StudentSerializer(student).data
                student_json["attendance"] = 1
                attendance_list[lecTime].append(student_json)

            for student in absent_students:
                student_json = StudentSerializer(student).data
                student_json["attendance"] = 0
                attendance_list[lecTime].append(student_json)

            attendance_list[lecTime].sort(key=lambda x: x["sapID"])

        final_attendance_list = []

        for lecTime in attendance_list:
            attendance_object = {}
            attendance_object['time'] = lecTime
            attendance_object['attendance_list'] = attendance_list[lecTime]
            final_attendance_list.append(attendance_object)

        response_data = {
            'attendance': final_attendance_list,
        }

        return JsonResponse(response_data, status=status.HTTP_200_OK)


class GetAttendanceOfRange(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        subject_name = kwargs['subject']
        div = kwargs['div']

        try:
            date_from = kwargs['date_from']
            d, m, y = date_from.split('-')
            date_from = datetime.datetime(int(y), int(m), int(d)).date()
        except KeyError:
            date_from = datetime.date.today()

        try:
            date_to = kwargs['date_to']
            d, m, y = date_to.split('-')
            date_to = datetime.datetime(int(y), int(m), int(d)).date()
        except KeyError:
            date_to = datetime.date.today()

        yearname, division = div.split("_")
        year = Div.yearnameToYear(yearname)

        if date_from.month < 6 and date_to.month < 6:
            semester = year * 2
        elif date_from.month >= 6 and date_to.month >= 6:
            semester = year * 2 - 1
        else:
            response_data = {'error_message': "Dates are not from the same semester."}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        try:
            subject = Subject.objects.get(name=subject_name)
            div = Div.objects.get(division=division, semester=semester, calendar_year=datetime.date.today().year)

        except Subject.DoesNotExist:
            response_data = {'error_message': "Subject " + subject_name + " Does Not Exist"}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Div.DoesNotExist:
            response_data = {'error_message': "Division " + div + " Does Not Exist"}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        teacher = Teacher.objects.get(user=request.user)

        if div.classteacher is teacher:
            lecs = Lecture.objects.filter(date__lte=date_to, date__gte=date_from, div=div, subject=subject)
        else:
            lecs = Lecture.objects.filter(date__lte=date_to, date__gte=date_from, teacher=teacher,
                                          div=div, subject=subject)

        # if lecs:
        #     student_list = Student.objects.filter(div=div)
        #     student_lectures = StudentLecture.objects.filter(lecture__in=lecs)

        #     attendance_list = []

        #     for student in student_list:
        #         relevant_student_lectures = student_lectures.filter(student=student)
        #         student_json = StudentSerializer(student).data
        #         student_json["attendance_count"] = len(relevant_student_lectures)
        #         student_json["attendance_percentage"] = len(relevant_student_lectures) * 100 / len(lecs)
        #         attendance_list.append(student_json)

        #     attendance_list.sort(key=lambda x: x["sapID"])

        #     response_data = {
        #         'attendance': attendance_list,
        #     }

        # else:
        #     response_data = {
        #         'attendance': [],
        #     }

        # return JsonResponse(response_data, status=status.HTTP_200_OK)
        attendance_list = {}

        for lec in lecs:
            lecDateTime = lec.getDateTimeString()
            attendance_list[lecDateTime] = []
            student_lecs = StudentLecture.objects.filter(lecture=lec)
            present_students = [sl.student for sl in student_lecs]

            student_divs = StudentDivision.objects.filter(division=div)
            div_students = [sd.student for sd in student_divs]

            absent_students = list(set(div_students) - set(present_students))

            for student in present_students:
                student_json = StudentSerializer(student).data
                student_json["attendance"] = 1
                attendance_list[lecDateTime].append(student_json)

            for student in absent_students:
                student_json = StudentSerializer(student).data
                student_json["attendance"] = 0
                attendance_list[lecDateTime].append(student_json)

            attendance_list[lecDateTime].sort(key=lambda x: x["sapID"])

        final_attendance_list = []

        for lecDateTime in attendance_list:
            attendance_object = {}
            attendance_object['time'] = lecDateTime
            attendance_object['attendance_list'] = attendance_list[lecDateTime]
            final_attendance_list.append(attendance_object)

        response_data = {
            'attendance': final_attendance_list,
        }

        return JsonResponse(response_data, status=status.HTTP_200_OK)


class GetAttendanceOfStudent(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        subject_name = kwargs['subject']
        student_sap = int(kwargs['sapID'])

        try:
            subject = Subject.objects.get(name=subject_name)
            student = Student.objects.get(sapID=student_sap)

        except Subject.DoesNotExist:
            response_data = {'error_message': "Subject " + subject_name + " Does Not Exist"}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Student.DoesNotExist:
            response_data = {'error_message': "Student with SAP " + str(student_sap) + " Does Not Exist"}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        divs = list(student.div.all())

        class_teacher_list = [div.classteacher for div in divs]

        teacher = Teacher.objects.get(user=request.user)

        if teacher in class_teacher_list:
            lecs = Lecture.objects.filter(div__in=divs, subject=subject)
        else:
            lecs = Lecture.objects.filter(teacher=teacher, div__in=divs, subject=subject)

        if lecs:
            lecs = list(lecs)
            lecs.sort(key=lambda x: x.date)

            attendance_list = []
            attendance_count = 0
            attendance_total = 0

            for lecture in lecs:
                lecture_json = LectureSerializer(lecture).data
                lecture_json["date"] = "-".join(lecture_json["date"].split('-')[::-1])
                try:
                    StudentLecture.objects.get(student=student, lecture=lecture)
                    lecture_json["attendance"] = 1
                    attendance_count += 1
                except StudentLecture.DoesNotExist:
                    lecture_json["attendance"] = 0

                attendance_total += 1
                attendance_list.append(lecture_json)

            attendance_percentage = attendance_count * 100 / attendance_total

            response_data = {
                'attendance': attendance_list,
                'attendance_count': attendance_count,
                'attendance_total': attendance_total,
                'attendance_percentage': attendance_percentage,
            }

        else:
            response_data = {
                'attendance': [],
            }

        return JsonResponse(response_data, status=status.HTTP_200_OK)


class EditAttendanceOfDay(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        subject_name = kwargs['subject']
        div = kwargs['div']

        try:
            form_data = json.loads(request.body.decode())
            attendance_list = form_data['attendance_list']
        except Exception:
            attendance_list = request.POST.get('attendance_list')

        try:
            date = kwargs['date']
            d, m, y = date.split('-')
            date = datetime.datetime(int(y), int(m), int(d)).date()
        except KeyError:
            date = datetime.date.today()

        yearname, division = div.split("_")
        year = Div.yearnameToYear(yearname)
        if date.month < 6:
            semester = year * 2
        else:
            semester = year * 2 - 1
        try:
            subject = Subject.objects.get(name=subject_name)
            div = Div.objects.get(division=division, semester=semester, calendar_year=datetime.date.today().year)

        except Subject.DoesNotExist:
            response_data = {'error_message': "Subject " + subject_name + " Does Not Exist"}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Div.DoesNotExist:
            response_data = {'error_message': "Division " + div + " Does Not Exist"}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        teacher = Teacher.objects.get(user=request.user)

        if div.classteacher is teacher:
            lecs = Lecture.objects.filter(date=date, div=div, subject=subject)
        else:
            lecs = Lecture.objects.filter(date=date, teacher=teacher, div=div, subject=subject)

        for attendance_object in attendance_list:
            current_lecture = None
            lecTime = attendance_object['time']
            for lec in lecs:
                if lec.getTimeString() == lecTime:
                    current_lecture = lec

            for student_entry in attendance_object['attendance_list']:
                student = Student.objects.get(sapID=student_entry['sapID'])
                if int(student_entry['attendance']) == 1:
                    StudentLecture.objects.get_or_create(student=student, lecture=current_lecture)
                else:
                    try:
                        sl = StudentLecture.objects.get(student=student, lecture=current_lecture)
                        sl.delete()
                    except StudentLecture.DoesNotExist:
                        pass

        response_data = {'success_message': 'Successfully saved attendance data'}
        return JsonResponse(response_data, status=status.HTTP_200_OK)


class DownloadCsv(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        subject_name = kwargs['subject']
        div = kwargs['div']

        try:
            date_from = kwargs['date_from']
            d, m, y = date_from.split('-')
            date_from = datetime.datetime(int(y), int(m), int(d)).date()
        except KeyError:
            date_from = datetime.date.today()

        try:
            date_to = kwargs['date_to']
            d, m, y = date_to.split('-')
            date_to = datetime.datetime(int(y), int(m), int(d)).date()
        except KeyError:
            date_to = datetime.date.today()

        yearname, division = div.split("_")
        year = Div.yearnameToYear(yearname)

        if date_from.month < 6 and date_to.month < 6:
            semester = year * 2
        elif date_from.month > 6 and date_to.month > 6:
            semester = year * 2 - 1
        else:
            response_data = {'error_message': "Dates are not from the same semester."}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        try:
            subject = Subject.objects.get(name=subject_name)
            div = Div.objects.get(division=division, semester=semester, calendar_year=datetime.date.today().year)

        except Subject.DoesNotExist:
            response_data = {'error_message': "Subject " + subject_name + " Does Not Exist"}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Div.DoesNotExist:
            response_data = {'error_message': "Division " + div + " Does Not Exist"}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        teacher = Teacher.objects.get(user=request.user)

        if div.classteacher is teacher:
            lecs = Lecture.objects.filter(date__lte=date_to, date__gte=date_from, div=div, subject=subject)
        else:
            lecs = Lecture.objects.filter(date__lte=date_to, date__gte=date_from, teacher=teacher,
                                          div=div, subject=subject)

        student_list = Student.objects.filter(div=div)
        student_lectures = StudentLecture.objects.filter(lecture__in=lecs)
        attendance_list = []
        for student in student_list:
            relevant_student_lectures = student_lectures.filter(student=student)
            student_json = StudentSerializer(student).data
            student_json["attendance_count"] = len(relevant_student_lectures)
            if lecs:
                student_json["attendance_percentage"] = len(relevant_student_lectures) * 100 / len(lecs)
            else:
                student_json["attendance_percentage"] = 100
            attendance_list.append(student_json)

        attendance_list.sort(key=lambda x: x["sapID"])

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'blob; filename="AttendanceData.csv"'

        csvwriter = csv.writer(response)

        csvwriter.writerow(attendance_list[0].keys())
        for var in attendance_list:
            csvwriter.writerow(var.values())

        return response

# Android EndPoint Views


class GetLectureListOfTheDay(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            date = kwargs['date']
            d, m, y = date.split('-')
            date = datetime.datetime(int(y), int(m), int(d)).date()
        except Exception:
            response_data = {'error_message': "Date sent is incorrectly formatted. Excepted dd-mm-yy format."}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        try:
            teacher = Teacher.objects.get(user=request.user)
        except Exception:
            response_data = {'error_message': "Logged in user is not a teacher."}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        ttlectures = TimeTableLecture.objects.filter(teacher=teacher, day_of_the_week=date.weekday())

        lectures = []

        for ttlecture in ttlectures:
            lecture = Lecture(
                roomNumber=ttlecture.roomNumber,
                startTime=ttlecture.startTime,
                endTime=ttlecture.endTime,
                date=date,
                teacher=ttlecture.teacher,
                div=ttlecture.div,
                subject=ttlecture.subject
            )
            lectures.append(lecture)

        lectures = LectureSerializer(lectures, many=True).data

        return JsonResponse({
            'date': date,
            'lectures': lectures
        }, status=status.HTTP_200_OK)


class GetStudentListOfLecture(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        subject_name = kwargs['subject']
        div = kwargs['div']

        yearname, division = div.split("_")
        year = Div.yearnameToYear(yearname)
        if datetime.date.today().month < 6:
            semester = year * 2
        else:
            semester = year * 2 - 1
        try:
            # subject = Subject.objects.get(name=subject_name)
            div = Div.objects.get(division=division, semester=semester, calendar_year=datetime.date.today().year)

        except Subject.DoesNotExist:
            response_data = {'error_message': "Subject " + subject_name + " Does Not Exist"}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Div.DoesNotExist:
            response_data = {'error_message': "Division " + div + " Does Not Exist"}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        students = Student.objects.filter(div=div)
        students_json = StudentSerializer(students, many=True).data

        for student in students_json:
            student['Attendance'] = 0
            student['sapID'] = str(student['sapID'])

        return JsonResponse({
            # 'subject': SubjectSerializer(subject).data,
            # 'div': DivSerializer(div).data,
            'students': students_json
        }, status=status.HTTP_200_OK)


class SaveAttendance(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            form_data = json.loads(request.body.decode())
            subject_name = form_data['subject']
            div = form_data['div']
            roomNumber = form_data['room']
            startTime = form_data['startTime']
            endTime = form_data['endTime']
            lecture_date = form_data['date']
            students = form_data['students']
        except KeyError:
            response_data = {'error_message': "Expecting subject, div, room, startTime, endTime, date and students."}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            subject_name = request.POST.get('subject')
            div = request.POST.get('div')
            roomNumber = request.POST.get('room')
            startTime = request.POST.get('startTime')
            endTime = request.POST.get('endTime')
            lecture_date = request.POST.get('date')
            students = request.POST.get('students')

        yearname, division = div.split("_")
        year = Div.yearnameToYear(yearname)
        if datetime.date.today().month < 6:
            semester = year * 2
        else:
            semester = year * 2 - 1
        try:
            subject = Subject.objects.get(name=subject_name)
            div = Div.objects.get(division=division, semester=semester, calendar_year=datetime.date.today().year)
            h, m, s = startTime.split(':')
            startTime = datetime.time(int(h), int(m), int(s))
            h, m, s = endTime.split(':')
            endTime = datetime.time(int(h), int(m), int(s))
            d, m, y = lecture_date.split('-')
            lecture_date = datetime.datetime(int(y), int(m), int(d)).date()
        except Subject.DoesNotExist:
            response_data = {'error_message': "Subject " + subject_name + " Does Not Exist"}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Div.DoesNotExist:
            response_data = {'error_message': "Division " + div + " Does Not Exist"}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            response_data = {'error_message': "Wrong Date and/or Time format. Expecting dd-mm-yy and hh:mm:ss"}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        lecture, _ = Lecture.objects.get_or_create(
            roomNumber=roomNumber,
            startTime=startTime,
            endTime=endTime,
            date=lecture_date,
            teacher=Teacher.objects.get(user=request.user),
            div=div,
            subject=subject
        )

        for student in students:
            student_object = Student.objects.get(sapID=int(student['sapID']))
            if student['Attendance'] == 1:
                StudentLecture.objects.get_or_create(student=student_object, lecture=lecture)
            else:
                try:
                    StudentLecture.objects.get(student=student_object, lecture=lecture).delete()
                except StudentLecture.DoesNotExist:
                    pass

        return JsonResponse({
            'subject': lecture.subject.name,
            'div': str(lecture.div),
            'room': lecture.roomNumber,
            'startTime': lecture.startTime.strftime('%H:%M:%S'),
            'endTime': lecture.endTime.strftime('%H:%M:%S'),
            'date': lecture.date.strftime('%d-%m-%Y')
        }, status=status.HTTP_200_OK)


class GetStudentsAttendance(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        student = Student.objects.get(user=user)
        student_divisions = StudentDivision.objects.filter(student=student)

        attendance = {}
        for sd in student_divisions:
            division = sd.division
            for subject in division.subject.all():
                lectures = Lecture.objects.filter(div=division, subject=subject)
                attendance[subject.name] = {
                    'type': division.get_class_type(),
                    'subject': subject.name,
                    'total': 0,
                    'attended': 0,
                }
                for lec in lectures:
                    attendance[subject.name]['total'] += 1
                    try:
                        StudentLecture.objects.get(student=student, lecture=lec)
                        attendance[subject.name]['attended'] += 1
                    except StudentLecture.DoesNotExist:
                        pass

        attendance_list = []
        for sub in attendance:
            attendance_list.append(attendance[sub])

        return JsonResponse({'attendance': attendance_list}, status=status.HTTP_200_OK)
