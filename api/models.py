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