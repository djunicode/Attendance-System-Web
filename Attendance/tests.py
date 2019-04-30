from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory
from .models import AppUser, Teacher, Student, Lecture, Div, Subject
import json
from rest_framework import status

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
        self.token = content['token']
        self.assertTrue(status.is_success(response.status_code))
