from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns=[
    path('password_reset/', auth_views.PasswordResetView.as_view()),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view()),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view()),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view()),
]