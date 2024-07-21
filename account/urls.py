from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, RegisterPage, logout_view

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
]
