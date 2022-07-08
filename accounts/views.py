from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate
from .models import User
# from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
# from django.views.generic.edit import CreateView
# from django.urls import reverse_lazy
# from django.views.generic import TemplateView
# Create your views here.
# 홈화면
def showmain(request):
    return render(request, 'accounts/base.html')

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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('showmain')
        else:
            return render(request, 'accounts/login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'accounts/login.html')

# 로그아웃
def logout(request):
    auth.logout(request)
    return render(request, 'accounts/logged_out.html')