from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory, force_authenticate
from .models import AppUser, Teacher, Student, Lecture, Div, Subject
import json
from rest_framework import status
from rest_framework.authtoken.models import Token

# Create your tests here.


class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.normal_user = AppUser.objects.create_user(
            username="PranitSir", password="pb@12345", email="pranit@djsce.in"
        )
        self.teacher = Teacher.objects.create(
            user=self.normal_user, teacherID=900015
        )

    def test_login_teacher(self):
        data = {'teacherId': 900015, 'password': "pb@12345"}
        response = self.client.post('/Attendance/login-teacher/', data, format='json', follow=True)
        content = json.loads(response.content)
        print(content)
        self.token = Token.objects.get(key=content['token'])
        self.assertTrue(status.is_success(response.status_code))

    def test_signup_teacher(self):
        data = {'teacherId': 900016, 'password': "ag@12345", 'fname': 'Ankit', 'lname': 'Gupta', 'spec': 'Everything'}
        response = self.client.post('/Attendance/signup-teacher/', data, format='json', follow=True)
        content = json.loads(response.content)
        print(content)
        self.token = Token.objects.get(key=content['token'])
        self.assertTrue(status.is_success(response.status_code))
