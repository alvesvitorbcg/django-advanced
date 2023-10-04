from django.contrib.auth.models import User, Group
from rest_framework import serializers
from core.models import VerificationStatus, Customer, Employee, Role, Status
from loan_application.models import LoanApplication
from verification_document.models import VerificationDocument


class BadRequest(BaseException):
    pass


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


def is_changing_status_forward(validated_data):
    status = validated_data.get('status')
    return status is Status.APPROVED.value or status is Status.REJECTED.value


def should_not_have_status_moved_forward(instance):
    return (instance.verifier is None or
            instance.reviewer is None or
            instance.verification_status is not VerificationStatus.VERIFIED.value)


class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class VerificationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationDocument
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
