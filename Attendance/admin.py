from django.contrib import admin
from .models import AppUser, Subject, Lecture, Div, Teacher, Student
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreateForm


class UserAdmin(BaseUserAdmin):
    add_form = UserCreateForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "is_student",
                    "is_teacher",
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


# Register your models here.
admin.site.register(AppUser, UserAdmin)
admin.site.register(Subject)
admin.site.register(Lecture)
admin.site.register(Div)
admin.site.register(Student)
admin.site.register(Teacher)
