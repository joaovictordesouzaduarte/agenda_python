from django.urls import path
from . import views

url_patterns = [
    path('', views.login, name='index_login'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('r egister/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
]