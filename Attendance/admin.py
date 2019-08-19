from django.contrib import admin
from .models import AppUser, Subject, Lecture, Div, Teacher, Student
from .models import SubjectTeacher, StudentLecture, StudentDivision
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreateForm
from datetime import date


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
    ordering = ['-calendar_year', 'semester', 'division']
    list_display = ['div', 'semester', 'get_class_type']
    search_fields = ['division']

    def div(self, obj):
        return str(obj)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        terms = search_term.replace('_', ' ').split(' ')
        queryset = self.model.objects.all()
        for term in terms:
            try:
                term_as_int = int(term)
                queryset &= self.model.objects.filter(semester=term_as_int)
            except ValueError:
                if term in ['FE', 'SE', 'TE', 'BE']:
                    if date.today().month < 6:
                        semester = Div.yearnameToYear(term) * 2
                    else:
                        semester = Div.yearnameToYear(term) * 2 - 1
                    queryset &= self.model.objects.filter(semester=semester)
                else:
                    queryset &= self.model.objects.filter(division__contains=term)
        return queryset, use_distinct


class LectureAdmin(admin.ModelAdmin):
    ordering = ['-date', '-endTime']
    list_display = ['lecturestring', 'date']
    search_fields = ['teacher__user__first_name', 'teacher__user__middle_name', 'teacher__user__last_name']
    search_fields.extend(['subject__name', 'date'])

    def lecturestring(self, obj):
        return str(obj)

    def get_search_results(self, request, queryset, search_term):
        qset, use_distinct = super().get_search_results(request, queryset, search_term)
        terms = search_term.replace('_', ' ').split(' ')
        queryset = self.model.objects.all()
        filtered = False
        for term in terms:
            if term in ['FE', 'SE', 'TE', 'BE']:
                if date.today().month < 6:
                    semester = Div.yearnameToYear(term) * 2
                else:
                    semester = Div.yearnameToYear(term) * 2 - 1
                queryset &= self.model.objects.filter(div__semester=semester)
                filtered = True
            elif term in ['A', 'B', 'A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4']:
                queryset &= self.model.objects.filter(div__division__contains=term)
                filtered = True
            else:
                queryset |= self.model.objects.filter(div__division__contains=term)
        if filtered:
            return qset | queryset, use_distinct
        else:
            return qset, use_distinct


class StudentAdmin(admin.ModelAdmin):
    ordering = ['-sapID']
    list_display = ['name', 'sapID']
    autocomplete_fields = ('user__username',)
    search_fields = ['user__first_name', 'user__middle_name', 'user__last_name', 'sapID']

    def name(self, obj):
        return obj.user.getfullname()


class TeacherAdmin(admin.ModelAdmin):
    ordering = ['teacherID']
    list_display = ['name', 'teacherID']
    autocomplete_fields = ('user__username',)
    search_fields = ['user__first_name', 'user__middle_name', 'user__last_name', 'teacherID']

    def name(self, obj):
        return obj.user.getfullname()


class SubjectTeacherAdmin(admin.ModelAdmin):
    ordering = ['-div__calendar_year', 'div__semester']
    search_fields = ['subject__name', 'teacher__teacherID']
    search_fields.extend(['teacher__user__first_name', 'teacher__user__middle_name', 'teacher__user__last_name'])

    def get_search_results(self, request, queryset, search_term):
        qset, use_distinct = super().get_search_results(request, queryset, search_term)
        terms = search_term.replace('_', ' ').split(' ')
        queryset = self.model.objects.all()
        filtered = False
        for term in terms:
            if term in ['FE', 'SE', 'TE', 'BE']:
                if date.today().month < 6:
                    semester = Div.yearnameToYear(term) * 2
                else:
                    semester = Div.yearnameToYear(term) * 2 - 1
                queryset &= self.model.objects.filter(div__semester=semester)
                filtered = True
            elif term in ['A', 'B', 'A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4']:
                queryset &= self.model.objects.filter(div__division__contains=term)
                filtered = True
            else:
                queryset |= self.model.objects.filter(div__division__contains=term)
        if filtered:
            return qset | queryset, use_distinct
        else:
            return qset, use_distinct


class StudentLectureAdmin(admin.ModelAdmin):
    ordering = ['-lecture__date', '-lecture__endTime', 'student__sapID']
    search_fields = ['lecture__teacher__user__first_name', 'lecture__teacher__user__middle_name']
    search_fields.extend(['lecture__subject__name', 'lecture__date', 'lecture__teacher__user__last_name'])
    search_fields.extend(['student__user__first_name', 'student__user__middle_name', 'student__user__last_name'])

    def get_search_results(self, request, queryset, search_term):
        qset, use_distinct = super().get_search_results(request, queryset, search_term)
        terms = search_term.replace('_', ' ').split(' ')
        queryset = self.model.objects.all()
        filtered = False
        for term in terms:
            if term in ['FE', 'SE', 'TE', 'BE']:
                if date.today().month < 6:
                    semester = Div.yearnameToYear(term) * 2
                else:
                    semester = Div.yearnameToYear(term) * 2 - 1
                queryset &= self.model.objects.filter(lecture__div__semester=semester)
                filtered = True
            elif term in ['A', 'B', 'A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4']:
                queryset &= self.model.objects.filter(lecture__div__division__contains=term)
                filtered = True
            else:
                queryset |= self.model.objects.filter(lecture__div__division__contains=term)
        if filtered:
            return qset | queryset, use_distinct
        else:
            return qset, use_distinct


class StudentDivisionAdmin(admin.ModelAdmin):
    ordering = ['-division__calendar_year', '-division__semester', 'student__sapID']
    search_fields = ['student__sapID']
    search_fields.extend(['student__user__first_name', 'student__user__middle_name', 'student__user__last_name'])

    def get_search_results(self, request, queryset, search_term):
        qset, use_distinct = super().get_search_results(request, queryset, search_term)
        terms = search_term.replace('_', ' ').split(' ')
        queryset = self.model.objects.all()
        filtered = False
        for term in terms:
            if term in ['FE', 'SE', 'TE', 'BE']:
                if date.today().month < 6:
                    semester = Div.yearnameToYear(term) * 2
                else:
                    semester = Div.yearnameToYear(term) * 2 - 1
                queryset &= self.model.objects.filter(division__semester=semester)
                filtered = True
            elif term in ['A', 'B', 'A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4']:
                queryset &= self.model.objects.filter(division__division__contains=term)
                filtered = True
            else:
                queryset |= self.model.objects.filter(division__division__contains=term)
        if filtered:
            return qset | queryset, use_distinct
        else:
            return qset, use_distinct


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
