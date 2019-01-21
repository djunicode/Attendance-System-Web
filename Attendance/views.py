from django.shortcuts import render
from django.urls import reverse_lazy
from . import forms
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import logout

class SignUp(CreateView):
    form_class = forms.UserCreateForm()
    success_url = reverse_lazy('login')
    template_name = 'Attendance/signup.html'

class HomePage(TemplateView):
    template_name = 'Attendance/index.html'

class TestPage(TemplateView):
    template_name = 'Attendance/login_success.html'

class ThanksPage(TemplateView):
    template_name = 'Attendance/logout_success.html'

#########################################################################################################

def login_user_teacher(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dash')
    return render(request, 'Attendance/login.html', context={'form': forms.TeacherLoginForm()})

class Dash(TemplateView):
    template_name = 'Attendance/login_success.html'

