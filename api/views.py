import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

from api.models import Employee, Transaction, Booking


def addBooking(request, employeeId, bookingId):
    if request.user.is_authenticated and request.method == "POST":
        transaction = Transaction.objects.create(employee_id=employeeId, booking_id=bookingId,
                                                 longitude=request.POST.get('lng'),
                                                 latitude=request.POST.get('lat'))
        transaction.save()

        employee = Employee.objects.filter(user=request.user)[0]
        transaction = Transaction.objects.filter(employee=employee).order_by('-timestamp')[0]

        context = {'employee': employee,
                   'transaction': transaction,
                   'availableBookings': transaction.booking.bookings.all(),
                   'message': 'The transaction was successful!'
                   }

        return redirect('dashboard')
    else:
        employee = Employee.objects.filter(user=request.user)[0]
        transaction = Transaction.objects.filter(employee=employee).order_by('-timestamp')[0]

        context = {'employee': employee,
                   'transaction': transaction,
                   'availableBookings': transaction.booking.bookings.all(),
                   'message': 'The transaction was successful!'}

        return render(request, 'accounts/dashboard.html', context)



class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(*args, **kwargs)
        employee = Employee.objects.filter(user = self.request.user)[0]
        transaction = Transaction.objects.filter(employee = employee).order_by('-timestamp')[0]

        context['employee'] = employee
        context['transaction'] = transaction
        context['availableBookings'] = transaction.booking.bookings.all()
        return context