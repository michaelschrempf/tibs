from django.contrib import admin

# Register your models here.
from django.contrib import admin

from . import models

admin.site.register(models.Booking)
admin.site.register(models.Employee)
admin.site.register(models.Transaction)
admin.site.register(models.Message)
admin.site.register(models.MessageState)
admin.site.register(models.MessageType)