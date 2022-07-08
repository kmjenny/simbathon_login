from .models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from pkg_resources import require
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

class CreateUserForm(forms.ModelForm):
    username = forms.CharField(
        label='아이디',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class' : 'username',
                'placeholder' : '아이디'
            }
        ),
        error_messages={'required' : '아이디를 입력해주세요'}
    )
    password1 = forms.CharField(
        label='비밀번호',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class' : 'password1',
                'placeholder' : '비밀번호'
            }
        ),
        error_messages={'required' : '비밀번호를 입력해주세요.'}
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class' : 'password2',
                'placeholder' : '비밀번호 확인'
            }
        ),
        error_messages={'required' : '비밀번호가 일치하지 않습니다.'}
    )
    email = forms.EmailField(
        label='이메일',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class' : 'email',
                'placeholder' : '이메일'
            }
        ),
        error_messages={'required' : '이메일을 입력해주세요.'}
    )
    nickname = forms.CharField(
        label='닉네임',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class' : 'nickname',
                'placeholder' : '닉네임'
            }
        ),
        error_messages={'required' : '닉네임을 입력해주세요.'}
    )

    field_order = [
        'username',
        'nickname',
        'email',
        'password1',
        'password2'
    ]

    class Meta:
        model=User
        fields = [
            'username',
            'nickname',
            'email',
            'password1'
        ]

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username', '')
        nickname = cleaned_data.get('nickname', '')
        email = cleaned_data.get('email', '')
        password1 = cleaned_data.get('password1', '')
        password2 = cleaned_data.get('password2', '')

        if password1 != password2 :
            return self.add_error('password2', '비밀번호가 다릅니다.')
        elif not (4<=len(username)<=16):
            return self.add_error('username', '아이디는 4~16자로 입력해 주세요.')
        elif 8 > len(password1):
            return self.add_error('password1', '비밀번호는 8자 이상으로 적어주세요.')
        elif not ((email.endswith('@dongguk.edu')) or (email.endswith('@dgu.edu')) or (email.endswith('@dgu.ac.kr'))):
            return self.add_error('email', '동국대학교 이메일로만 가입이 가능합니다.')
        else:
            self.username = username
            self.nickname = nickname
            self.email = email
            self.password1 = PasswordHasher().hash(password1)
            self.password2 = password2

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=32,
        label='아이디',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class' : 'username',
                'placeholder' : '아이디'
            }
        ),
        error_messages={'required' : '아이디를 입력해주세요.'}
    )

    password1 = forms.CharField(
        max_length=128,
        label='비밀번호',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class' : 'password1',
                'placeholder' : '비밀번호'
            }
        ),
        error_messages={'required' : '비밀번호를 입력해주세요.'}
    )

    field_order = [
        'username',
        'password1'
    ]

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username', '')
        password1 = cleaned_data.get('password1', '')

        if username == '':
            return self.add_error('username', '아이디를 다시 입력해 주세요.')
        elif password1 == '':
            return self.add_error('password1', '비밀번호를 다시 입력해 주세요.')
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return self.add_error('username', '아이디가 존재하지 않습니다.')

            try:
                PasswordHasher().verify(user.password1, password1)
            except VerifyMismatchError:
                return self.add_error('password1', '비밀번호가 다릅니다.')

            self.login_session = user.username
