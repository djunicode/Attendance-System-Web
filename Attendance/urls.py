from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'Attendance'

urlpatterns = [
    path('login/', views.login_user_teacher, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('home_dashboard/', views.dash, name='dash'),
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
]
