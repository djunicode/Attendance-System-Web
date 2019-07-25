from rest_framework import serializers
from .models import Teacher, Student, Lecture, Div, Subject


class TeacherSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='__str__')

    class Meta:

        model = Teacher
        fields = ('name', 'specialization', 'teacherID', 'subject')


class ShortTeacherSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='__str__')
    sapID = serializers.CharField(source='teacherID')

    class Meta:

        model = Teacher
        fields = ('name', 'specialization', 'sapID')


class StudentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='__str__')

    class Meta:
        model = Student
        fields = ('name', 'sapID')


class DivSerializer(serializers.ModelSerializer):
    classteacher = serializers.StringRelatedField()
    class_type = serializers.CharField(source='get_class_type')

    class Meta:
        model = Div
        fields = ('division', 'class_type', 'classteacher', 'semester', 'calendar_year')


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('name', 'semester', 'subjectCode')


class LectureSerializer(serializers.ModelSerializer):
    timing = serializers.CharField(source='getTimeString')
    div = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()
    subject = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Lecture
        fields = ('roomNumber', 'timing', 'date', 'subject', 'teacher', 'div')
