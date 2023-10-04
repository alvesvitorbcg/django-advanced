from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api import models
from api.models import LoanApplication, VerificationDocument, VerificationStatus, Customer, Employee, Role, Status


class BadRequest(BaseException):
    pass


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
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

    # def create(self, validated_data):
    #     validated_data.pop('verification_status', None)
    #     validated_data.pop('status', None)
    #     validated_data.pop('reviewer', None)
    #     validated_data.pop('verifier', None)
    #     loan_application = LoanApplication.objects.create(
    #         **validated_data)
    #     return loan_application

    # def update(self, instance, validated_data):
    #     if (validated_data.get('verification_status') is VerificationStatus.ASSIGNED.value and validated_data.get('verifier') is None):
    #         raise BadRequest(
    #             "Verification status cannot be changed to ASSIGNED without verifier")

    #     if (validated_data.get('verification_status') is VerificationStatus.VERIFIED.value and instance.verifier is None):
    #         raise BadRequest(
    #             "Verification status cannot be changed to VERIFIED because it was not assigned to verifier")
    #     # documents = VerificationDocument.objects.filter(
    #     #     loan_application=instance)
    #     # print(documents)
    #     if (validated_data.get('verification_status') is VerificationStatus.VERIFIED.value and instance.verifier is None):
    #         raise BadRequest(
    #             "Verification status cannot be changed to VERIFIED because it was not assigned to verifier")

    #     if (is_changing_status_forward(validated_data) and should_not_have_status_moved_forward(instance)):
    #         raise BadRequest(
    #             "Status cannot be changed to ASSIGNED without verifier, reviewer and verification status as VERIFIED")

    #     if (validated_data.get('verifier') is not None):
    #         setattr(instance, 'verifier', validated_data.get('verifier'))
    #         setattr(instance, 'verification_status',
    #                 VerificationStatus.ASSIGNED.value)
    #     # if(instance.verification_status is VerificationStatus.VERIFIED.value and
    #     #         validated_data.get('reviewer') is not None):
    #     #     setattr(instance, 'reviewer', validated_data.get('reviewer'))
    #     #     setattr(instance, 'verification_status',
    #     #             VerificationStatus.ASSIGNED.value)
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
