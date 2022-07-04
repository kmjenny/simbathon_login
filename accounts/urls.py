from django.urls import path
from .views import *
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.CreateUserView.as_view(), name='signup'),
    path('signup/done', views.RegisteredView.as_view(), name="create_user_done"),
]