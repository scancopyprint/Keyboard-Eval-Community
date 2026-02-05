from django.urls import path
from . import views

urlpatterns = [
    path('login.html', views.tologinpage, name='toLoginPage'),
    path('register.html', views.toregisterpage, name='toRegisterPage')
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
]