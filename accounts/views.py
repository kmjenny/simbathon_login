from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.views.generic import TemplateView

# Create your views here.
# 홈화면
def showmain(request):
    return render(request, 'accounts/base.html')

# 회원가입
def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                username = request.POST['username'],

                password = request.POST['password1'],
                email = request.POST['email'],
            )
            auth.login(request, user)
            return redirect('/')
        return render(request, 'signup.html')
    else:
        form = CreateUserForm
        return render(request, 'accounts/signup.html', {'form':form})

class CreateUserView(CreateView):
    template_name = 'accounts/signup.html'
    form = UserCreationForm
    success_url = reverse('create_user_done')

class RegisteredView(TemplateView):
    template_name = 'accounts/signup_done.html'

# # 로그인
# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('board')
#         else:
#             return render(request, 'login.html', {'error': 'username or password is incorrect.'})
#     else:
#         return render(request, 'login.html')

# # 로그아웃
# def logout(request):
#     auth.logout(request)
#     return redirect('base.html')