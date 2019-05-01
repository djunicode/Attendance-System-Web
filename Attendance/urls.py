from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'Attendance'

urlpatterns = [
    path('login/', views.login_user_teacher, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('thanks/', views.ThanksPage.as_view(), name='thanks'),

    path('teachers/', views.TeacherListView.as_view(), name='teacher-list'),
    path('teachers/<int:pk>/', views.TeacherDetailView.as_view(), name='teacher-details'),
    path('students/', views.StudentListView.as_view(), name='student-list'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student-details'),
    path('subjects/', views.SubjectListView.as_view(), name='subject-list'),
    path('subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='subject-details'),
    path('lectures/', views.LectureListView.as_view(), name='lecture-list'),
    path('lectures/<int:pk>/', views.LectureDetailView.as_view(), name='lecture-details'),
    path('divisions/', views.DivisionListView.as_view(), name='division-list'),
    path('divisions/<int:pk>/', views.DivisionDetailView.as_view(), name='division-details'),

    path('login-teacher/', views.LoginTeacherView.as_view(), name='login-teacher'),
    path('logout-teacher/', views.LogoutTeacherView.as_view(), name='logout-teacher'),
    path('signup-teacher/', views.SignUpTeacherView.as_view(), name='signup-teacher'),
    path('dashboard-teacher/<int:teacherId>', views.TeachersSubjectDataView.as_view(), name='dashboard-teacher'),
    path('get-attendance-of-day/<str:subject>/<str:div>/<str:date>',
         views.GetAttendanceOfDay.as_view(), name='day-attendance'),
    path('get-attendance-of-range/<str:subject>/<str:div>/<str:date_from>/<str:date_to>',
         views.GetAttendanceOfRange.as_view(), name='range-attendance'),
    path('get-attendance-of-student/<str:subject>/<int:sapID>',
         views.GetAttendanceOfStudent.as_view(), name='student-attendance'),
    path('edit-attendance-of-day/<str:subject>/<str:div>/<str:date>',
         views.EditAttendanceOfDay.as_view(), name='edit-attendance'),
]
