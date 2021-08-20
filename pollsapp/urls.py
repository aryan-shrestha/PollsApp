from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'pollsapp'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:pk>/', views.detail, name = 'detail'),
    path('<int:pk>/vote', views.vote, name = 'vote'),
    path('add_polls/', views.add_polls, name = 'add_polls'),

    path('login/', views.user_login, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('logout/', views.user_logout, name = 'logout'),

    path('my_polls/', views.my_polls, name = 'my_polls'),
    path('<int:pk>/result', views.result, name = 'result'),
]

