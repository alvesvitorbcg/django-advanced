from django.contrib import admin
from api import models

# Register your models here.
admin.site.register(models.Customer)
admin.site.register(models.LoanApplication)
admin.site.register(models.Employee)
admin.site.register(models.Role)
