from django.contrib import admin
from core import models
from loan_application.models import LoanApplication

admin.site.register(models.Customer)
admin.site.register(LoanApplication)
admin.site.register(models.Employee)
admin.site.register(models.Role)
