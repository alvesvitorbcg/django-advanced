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


class LoanApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.LoanApplication
        fields = '__all__'
