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
from .models import Teacher, Student, Lecture, Div, Subject, SubjectTeacher, AppUser, StudentLecture, StudentDivision
from .serializers import TeacherSerializer, StudentSerializer, LectureSerializer, DivSerializer, SubjectSerializer
from rest_framework.authentication import TokenAuthentication
import datetime


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

        divisions = Div.objects.filter(classteacher=teacher)
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

        form_data = json.loads(request.body.decode())

        teacherID = form_data['teacherId']
        password = form_data['password']

        teacher = Teacher.objects.get(teacherID=teacherID)
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


# class RandomView(generics.GenericAPIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request, *args, **kwargs):
#         # return JsonResponse({
#         #     'success': True,
#         # })

#         print("\n\nForm Data:")
#         print(request.body)
#         print("\n\n")

#         form_data = json.loads(request.body.decode())

class SignUpTeacherView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):

        form_data = json.loads(request.body.decode())

        teacherId = form_data['teacherId']
        password = form_data['password']
        f_name = form_data['fname']
        l_name = form_data['lname']
        specialization = form_data['spec']
        # email = form_data['email']

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


class GetAttendanceOfDay(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        subject = kwargs['subject']
        div = kwargs['div']
        try:
            date = kwargs['date']
            d, m, y = date.split('\\')
            date = datetime.datetime(y, m, d).date()
        except KeyError:
            date = datetime.date.today()

        subject_code, subject_name = subject.split(': ')
        yearname, division = div.split("_")

        try:
            subject = Subject.objects.get(subjectCode=subject_code, subject_name=subject_name)
            div = Div.objects.get(division=division, year=yearname)

        except Subject.DoesNotExist:
            response_data = {'error_message': "Subject " + subject_name + " Does Not Exist"}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        except Div.DoesNotExist:
            response_data = {'error_message': "Division " + div + " Does Not Exist"}
            return JsonResponse(response_data, status=status.HTTP_400_BAD_REQUEST)

        print(date, subject_code, subject_name, yearname, division)

        teacher = Teacher.objects.get(user=request.user)

        lecs = Lecture.objects.filter(date=date, teacher=teacher, div=div, subject=subject)
        if lecs:
            student_lecs = StudentLecture.objects.filter(lecture__in=lecs)
            present_students = [sl.student for sl in student_lecs]

            student_divs = StudentDivision.objects.filter(division=div)
            div_students = [sd.student for sd in student_divs]

            absent_students = list(set(div_students) - set(present_students))

            attendance_list = []

            for student in present_students:
                student_json = StudentSerializer(student).data
                student_json["attendance"] = 1
                attendance_list.append(student_json)

            for student in absent_students:
                student_json = StudentSerializer(student).data
                student_json["attendance"] = 0
                attendance_list.append(student_json)
            attendance_list.sort(key=lambda x: x["sapID"])

            response_data = {
                'attendance': attendance_list,
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)

        else:
            response_data = {'error_message': "No Lectures on this day"}
            return JsonResponse(response_data, status=status.HTTP_200_OK)

        response_data = {}

        return JsonResponse(response_data, status=status.HTTP_200_OK)
