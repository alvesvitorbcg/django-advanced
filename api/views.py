from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status, serializers as rest_serializers
from rest_framework.response import Response
from api import serializers
from api import models


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class LoanApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.LoanApplication.objects.all()
    serializer_class = serializers.LoanApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    """"
    Performs create operation with enforced property values
    """

    def perform_create(self, serializer):
        serializer.save(
            status=models.Status.NEW.value,
            verification_status=models.VerificationStatus.PENDING.value,
            reviewer=None,
            verifier=None
        )

    def perform_update(self, serializer):
        verifier = serializer.validated_data.get('verifier')
        reviewer = serializer.validated_data.get('reviewer')
        verification_status = serializer.validated_data.get(
            'verification_status')

        if verification_status == models.VerificationStatus.ASSIGNED.value and verifier is None:
            raise rest_serializers.ValidationError(
                {"detail": "Verification status can only be 'Assigned' if a verifier is specified."},
            )

        serializer.save()


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleSerializer
    permission_classes = [permissions.IsAuthenticated]
