from socket import fromshare
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .validators import validate_symbols

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_symbols])
    nickname = forms.CharField(required=True)

    class Meta:
        model=User
        fields = ("username", "nickname", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CreateUserForm,self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.nickname = self.cleaned_data["nickname"]
        if commit:
            user.save()
        return user