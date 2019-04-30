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
        data = {'teacherID': 90000000015, 'password': "pass@123"}
        response = self.client.post('/Attendance/login-teacher/', data, format='json', follow=True)
        content = json.loads(response.content)
        print(content)
        self.token = content['token']
        self.assertTrue(status.is_success(response.status_code))
        response2 = self.client.get('/Attendance/random/', format='json', follow=True, HTTP_AUTHORIZATION=self.token)
        content2 = json.loads(response2.content)
        print(content2)
        self.assertTrue(status.is_success(response2.status_code))
