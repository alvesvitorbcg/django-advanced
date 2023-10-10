from rest_framework import viewsets, permissions
from api import serializers
from employee.models import Employee, Role


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = serializers.RoleSerializer
    permission_classes = [permissions.IsAuthenticated]
