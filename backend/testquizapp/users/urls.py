from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('signin/', views.LoginUserView.as_view(), name='login'),
    path('signup/', views.RegistrationView.as_view(), name='register'),

    path('logout/', LogoutView.as_view(), name='logout'),
]