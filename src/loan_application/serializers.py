from django.contrib.auth.models import User, Group
from rest_framework import serializers
from employee.models import Employee, Role
from customer.models import Customer
from loan_application.models import LoanApplication, LoanApplicationHistory
from verification_document.models import VerificationDocument


class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = '__all__'


class LoanApplicationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplicationHistory
        fields = '__all__'
