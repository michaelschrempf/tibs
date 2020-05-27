from django.urls import path
from django.contrib.auth import views as auth_views
from api import views as api_views
from . import views

urlpatterns = [
    path('', api_views.DashboardView.as_view(), name='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]