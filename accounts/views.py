from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate
from .models import User
# from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, LoginForm
# from django.views.generic.edit import CreateView
# from django.urls import reverse_lazy
# from django.views.generic import TemplateView
# Create your views here.
# 홈화면
def showmain(request):
    context = {}

    login_session = request.session.get('login_session', '')

    if login_session == '':
        context['login_session'] = False
    else:
        context['login_session'] = True

    return render(request, 'accounts/base.html', context)

# 회원가입
def signup(request):
    signup_form = CreateUserForm()
    context = {'forms':signup_form}
    if request.method == 'POST':
        signup_form = CreateUserForm(request.POST)
        if signup_form.is_valid():
            user = User(
                username = signup_form.username,
                nickname = signup_form.nickname,
                email = signup_form.email,
                password1 = signup_form.password1
            )
            user.save()
            return render(request, 'accounts/signup_done.html')
        else:
            context['forms'] = signup_form
            if signup_form.errors:
                for value in signup_form.errors.values():
                    context['error']=value
        return render(request, 'accounts/signup.html', context)
    else:
        return render(request, 'accounts/signup.html', context)

# class CreateUserView(CreateView):
#     template_name = 'accounts/signup.html'
#     form = UserCreationForm
#     success_url = reverse_lazy('create_user_done')

# class RegisteredView(TemplateView):
#     template_name = 'accounts/signup_done.html'

# 로그인
def login(request):
    loginform = LoginForm()
    context = { 'forms': loginform }
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        
        if loginform.is_valid():
            request.session['login_session'] = loginform.login_session
            request.session.set_expiry(0)
            return redirect('/')
        else:
            context['forms']=loginform
            if loginform.errors:
                for value in loginform.errors.values():
                    context['error'] = value
        return render(request, 'accounts/login.html', context)
    else:
        return render(request, 'accounts/login.html', context)

# 로그아웃
def logout(request):
    request.session.flush()
    return render(request, 'accounts/logged_out.html')