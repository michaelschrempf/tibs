import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

from api.models import Employee, Transaction, Booking, MessageEmployee, Message, MessageState


def addBooking(request, employeeId, bookingId):

    if not request.user.is_authenticated:
        return redirect('dashboard')


    employee = Employee.objects.filter(user=request.user)[0]

    if Transaction.objects.filter(employee=employee).count() > 0:
        transaction = Transaction.objects.filter(employee=employee).order_by('-timestamp')[0]

        if Booking.objects.filter(id=bookingId)[0] not in transaction.booking.bookings.all():
            employeeMessage = MessageEmployee.objects.create(employee=employee,
                                                             message=Message.objects.filter(idName="doublebooking")[0],
                                                             messageState=MessageState.objects.filter(name="Created")[0]
                                                             )

            employeeMessage.save()

            return redirect('dashboard')



    if request.user.is_authenticated and request.method == "POST":
        transaction_save = Transaction.objects.create(employee_id=employeeId, booking_id=bookingId,
                                                 longitude=request.POST.get('lng'),
                                                 latitude=request.POST.get('lat'))
        transaction_save.save()

        employeeMessage = MessageEmployee.objects.create(employee=employee,
                                                         message=Message.objects.filter(idName="bookingsuccess")[0],
                                                         messageState=MessageState.objects.filter(name="Created")[0]
                                                         )

        employeeMessage.save()

        return redirect('dashboard')
    else:
        return redirect('dashboard')






class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(*args, **kwargs)
        employee = Employee.objects.filter(user = self.request.user)[0]



        if Transaction.objects.filter(employee=employee).count() > 0:
            transaction = Transaction.objects.filter(employee=employee).order_by('-timestamp')[0]
            context['transaction'] = transaction

            context['availableBookings'] = transaction.booking.bookings.all()
        else:
            context['availableBookings'] = Booking.objects.filter(id=1)

        if MessageEmployee.objects.filter(employee=employee, messageState=MessageState.objects.filter(name="Created")[0]).count() > 0:
            messageEmployees = MessageEmployee.objects.filter(employee=employee, messageState=MessageState.objects.filter(name="Created")[0])
            for message in messageEmployees:
                message.messageState = MessageState.objects.filter(name="Showed")[0]
                message.save()
            context['messages'] = messageEmployees


        context['employee'] = employee

        return context


class MyBookingsView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/mybookings.html"

    def get_context_data(self, *args, **kwargs):
        context = super(MyBookingsView, self).get_context_data(*args, **kwargs)
        employee = Employee.objects.filter(user = self.request.user)[0]

        if Transaction.objects.filter(employee=employee).count() > 0:
            transactions_come = Transaction.objects.filter(employee=employee,
                                                           booking__name="Kommen").order_by('-timestamp')

        for transaction_come in transactions_come:
            transaction_end = Transaction.objects.filter(employee=employee, booking__name="Gehen",
                                                         timestamp__gte=transaction_come.timestamp)[0]

            



        context['employee'] = employee

        return context