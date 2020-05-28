from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('<int:employeeId>/bookings/<int:bookingId>/', views.addBooking, name='addBooking'),
    path('', views.DashboardView.as_view(), name='dashboard')
]