from rest_framework import serializers
from .models import Teacher, Student, Lecture, Div, Subject, TimeTableLecture


class TeacherSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='getfullname')

    class Meta:

        model = Teacher
        fields = ('name', 'specialization', 'teacherID', 'subject')


class StudentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='getfullname')

    class Meta:
        model = Student
        fields = ('name', 'sapID')


class LectureSerializer(serializers.ModelSerializer):
    timing = serializers.CharField(source="__str__")

    class Meta:
        model = Lecture
        fields = ('roomNumber', 'timing', 'date', 'subject', 'teacher')


class TimeTableLectureSerializer(serializers.ModelSerializer):
    timing = serializers.CharField(source="__str__")

    class Meta:
        model = TimeTableLecture
        fields = ('roomNumber', 'timing', 'day_of_the_week', 'subject', 'teacher')


class DivSerializer(serializers.ModelSerializer):

    class Meta:
        model = Div
        fields = ('division', 'classteacher', 'semester')


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('name', 'semester', 'subjectCode')
