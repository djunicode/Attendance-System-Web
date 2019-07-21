from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'Attendance'

urlpatterns = [
    path('login/', views.login_user_teacher, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('thanks/', views.ThanksPage.as_view(), name='thanks'),

    # Web URLs

    path('login-teacher/', views.LoginTeacherView.as_view(), name='login-teacher'),
    path('logout-teacher/', views.LogoutTeacherView.as_view(), name='logout-teacher'),
    path('signup-teacher/', views.SignUpTeacherView.as_view(), name='signup-teacher'),
    path('generic-login/', views.GenericLoginView.as_view(), name='generic-login'),
    path('dashboard-teacher/<int:teacherId>', views.TeachersSubjectDataView.as_view(), name='dashboard-teacher'),
    path('get-attendance-of-day/<str:subject>/<str:div>/<str:date>',
         views.GetAttendanceOfDay.as_view(), name='day-attendance'),
    path('get-attendance-of-range/<str:subject>/<str:div>/<str:date_from>/<str:date_to>',
         views.GetAttendanceOfRange.as_view(), name='range-attendance'),
    path('get-attendance-of-student/<str:subject>/<int:sapID>',
         views.GetAttendanceOfStudent.as_view(), name='student-attendance'),
    path('edit-attendance-of-day/<str:subject>/<str:div>/<str:date>',
         views.EditAttendanceOfDay.as_view(), name='edit-attendance'),
    path('get_csv/<str:subject>/<str:div>/<str:date_from>/<str:date_to>', views.DownloadCsv.as_view(), name='get-csv'),

    # Android URLs

    path('get-lectures-of-the-day/<str:date>', views.GetLectureListOfTheDay.as_view(), name='get-lectures'),
    path('get-student-list/<str:subject>/<str:div>/<str:date>/<str:startTime>', views.GetStudentListOfLecture.as_view(),
         name='get-students-list'),
    path('save-attendance/', views.SaveAttendance.as_view(), name='save-attendance'),
    path('get-students-attendance/', views.GetStudentsAttendance.as_view(), name='get-students-attendance'),
    path('get-students-attendance-history/<str:subject>/<str:type>', views.GetStudentAttendanceHistory.as_view(),
         name='get-students-attendance-history'),
    path('get-all-subjects-and-divisions/', views.GetSubjectsAndDivisions.as_view(),
         name='get-all-subjects-and-divisions'),
    path('save-lecture-and-get-student-list/', views.SaveLectureAndGetStudentsList.as_view(), name='save-lecture'),
    path('delete-lecture/', views.DeleteLecture.as_view(), name='delete-lecture')
]
