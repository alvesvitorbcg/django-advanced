from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api import models


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
        model = models.Customer
        fields = '__all__'


class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LoanApplication
        fields = '__all__'

    def create(self, validated_data):
        validated_data.pop('verification_status', None)
        validated_data.pop('status', None)
        validated_data.pop('reviewer', None)
        validated_data.pop('verifier', None)
        loan_application = models.LoanApplication.objects.create(
            **validated_data)
        return loan_application


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Employee
        fields = '__all__'


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'
