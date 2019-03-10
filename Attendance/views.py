from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from . import forms
from django.views.generic import TemplateView
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required

from rest_framework import generics
from .models import Teacher, Student, Lecture, Div, Subject
from .serializers import TeacherSerializer, StudentSerializer, LectureSerializer, DivSerializer, SubjectSerializer


class HomePage(TemplateView):
    template_name = 'Attendance/index.html'


class TestPage(TemplateView):
    template_name = 'Attendance/login_success.html'


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
