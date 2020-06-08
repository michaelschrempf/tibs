from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
    first_name = models.CharField(max_length=200)
    family_name = models.CharField(max_length=200)
    id_card = models.CharField(max_length=2048)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.first_name + " " + self.family_name


class Transaction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    booking = models.ForeignKey("Booking", on_delete=models.CASCADE)
    longitude = models.CharField(max_length=2000, blank=True)
    latitude = models.CharField(max_length=2000, blank=True)

    def __str__(self):
        return self.employee.family_name + "_" + self.booking.name + "_" + str(self.timestamp)


class Booking(models.Model):
    name = models.CharField(max_length=200)
    bookings = models.ManyToManyField("Booking", blank=True)

    def __str__(self):
        return self.name


class MessageType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class MessageState(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Message(models.Model):
    message = models.CharField(max_length=2000)
    idName = models.CharField(max_length=200, null=True, blank=True)
    messageType = models.ForeignKey("MessageType", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.message

class MessageEmployee(models.Model):
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    message = models.ForeignKey("Message", on_delete=models.CASCADE)
    messageState = models.ForeignKey("MessageState", on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.family_name + ": " + self.message.message



