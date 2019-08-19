from django.contrib import admin
from .models import AppUser, Subject, Lecture, Div, Teacher, Student
from .models import SubjectTeacher, StudentLecture, StudentDivision
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreateForm
from datetime import datetime, timedelta, date


class AppUserAdmin(UserAdmin):
    ordering = ['is_teacher', '-id']
    add_form = UserCreateForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": (
            "middle_name",
            "is_student",
            "is_teacher"
        )},),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "first_name",
                "middle_name",
                "last_name",
                "is_student",
                "is_teacher",
                "username",
                "password1",
                "password2",
            )},),
    )


class SubjectAdmin(admin.ModelAdmin):
    ordering = ['semester', 'name']
    search_fields = ['name', 'semester']


class DivAdmin(admin.ModelAdmin):
    ordering = ['-calendar_year', 'division']
    list_display = ['divstring', 'get_class_type']
    search_fields = ['divstring']

    def divstring(self, obj):
        return str(obj)


class LectureAdmin(admin.ModelAdmin):
    ordering = ['-date', '-endTime']
    list_display = ['lecturestring', 'date']
    search_fields = ['lecturestring', 'date']

    def lecturestring(self, obj):
        return str(obj)


class StudentAdmin(admin.ModelAdmin):
    ordering = ['-sapID']
    list_display = ['name', 'sapID']
    search_fields = ['user__first_name', 'user__middle_name', 'user__last_name', 'sapID']

    def name(self, obj):
        return obj.getfullname()


class TeacherAdmin(admin.ModelAdmin):
    ordering = ['teacherID']
    list_display = ['name', 'teacherID']
    search_fields = ['user__first_name', 'user__middle_name', 'user__last_name', 'teacherID']

    def name(self, obj):
        return obj.getfullname()


class SubjectTeacherAdmin(admin.ModelAdmin):
    ordering = ['-div__calendar_year', 'div__semester_order', 'div__semester']
    search_fields = ['subjectteacherstring']

    def subjectteacherstring(self, obj):
        return str(obj)


class StudentLectureAdmin(admin.ModelAdmin):
    ordering = ['-lecture__date', '-lecture__endTime', 'student__sapID']
    search_fields = ['studentstring', 'lecturestring', 'date']

    def studentstring(self, obj):
        return str(obj.student)

    def lecturestring(self, obj):
        return str(obj.lecture)


class StudentDivisionAdmin(admin.ModelAdmin):
    ordering = ['-division__calendar_year', 'division__semester_order', '-div__semester', 'student__sapID']
    search_fields = ['studentstring', 'lecturestring', 'date']

    def studentstring(self, obj):
        return str(obj.student)

    def lecturestring(self, obj):
        return str(obj.lecture)


# Register your models here.
admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Div, DivAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(SubjectTeacher, SubjectTeacherAdmin)
admin.site.register(StudentLecture, StudentLectureAdmin)
admin.site.register(StudentDivision, StudentDivisionAdmin)
