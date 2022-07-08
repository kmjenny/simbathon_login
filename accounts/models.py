from abc import abstractclassmethod
import email
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=32, unique=True, verbose_name='아이디')
    password1 = models.CharField(max_length=128, verbose_name='비밀번호')
    nickname = models.CharField(max_length=16, unique=True, verbose_name='닉네임')
    email = models.EmailField(max_length=128, unique=True, verbose_name='이메일')

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = 'user'
        verbose_name= '유저'
        verbose_name_plural = '유저'