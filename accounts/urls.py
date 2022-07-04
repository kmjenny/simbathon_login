from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
    # path('signup/', CreateUserView.as_view(), name='signup'),
    # path('signup/done/', RegisteredView.as_view(), name='create_user_done'),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('signup/', signup, name="signup"),
]