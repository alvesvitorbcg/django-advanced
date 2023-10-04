from django.contrib import admin
from loan_application.models import LoanApplication
from customer.models import Customer
from employee.models import Employee, Role

admin.site.register(Customer)
admin.site.register(LoanApplication)
admin.site.register(Employee)
admin.site.register(Role)
