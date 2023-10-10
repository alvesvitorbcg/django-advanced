from django.contrib import admin
from loan_application.models import LoanApplication, LoanApplicationHistory

admin.site.register(LoanApplication)
admin.site.register(LoanApplicationHistory)
