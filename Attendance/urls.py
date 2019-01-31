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
]
