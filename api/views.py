from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status as rest_status, serializers as rest_serializers
from rest_framework.response import Response
from api import serializers
from core import models
from loan_application.models import LoanApplication
from verification_document.models import VerificationDocument


def is_result_status(status):
    return status is models.Status.APPROVED.value or status is models.Status.REJECTED.value


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


def is_result_status(status):
    return status is models.Status.APPROVED.value or status is models.Status.REJECTED.value


def is_assigned(verification_status):
    return verification_status == models.VerificationStatus.ASSIGNED.value


def is_verified(verification_status):
    return verification_status == models.VerificationStatus.VERIFIED.value

# def is_pending(verification_status):
#     return verification_status == models.VerificationStatus.PENDING.value


def is_verification_result_status(verification_status):
    return verification_status == models.VerificationStatus.VERIFIED.value or verification_status == models.VerificationStatus.FAILED.value


class LoanApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = LoanApplication.objects.all()
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
        instance = serializer.instance
        verifier = serializer.validated_data.get('verifier')
        reviewer = serializer.validated_data.get('reviewer')
        verification_status = serializer.validated_data.get(
            'verification_status')
        status = serializer.validated_data.get(
            'status')

        if is_assigned(verification_status) and not instance.has_verifier and verifier is None:
            raise rest_serializers.ValidationError(
                {"detail": "Verification status can only be 'Assigned' if a Verifier is assigned to the Loan Application."},
            )

        if is_verification_result_status(verification_status) and not instance.has_verifier:
            raise rest_serializers.ValidationError(
                {"detail": "Verification status can only be 'Verified' or 'Failed' if a Verifier had been previously assigned."},
            )

        if is_result_status(status) and (not instance.has_reviewer or not instance.has_verifier or not instance.is_verification_status_verified):
            raise rest_serializers.ValidationError(
                {"detail": "Status can only be 'Approved' or 'Rejected' if a reviewer and a verifier had been previouly assigned and the verification status is 'Verified'."},
            )

        if reviewer is not None and not instance.has_reviewer and not instance.is_verification_status_verified:
            raise rest_serializers.ValidationError(
                {"detail": "Reviewer can only be assigned if the verification status is 'Verified'."},
            )

        if is_verified(verification_status):
            verification_documents = models.VerificationDocument.objects.filter(
                loan_application=instance)

            if len(verification_documents) == 0:
                raise rest_serializers.ValidationError(
                    {"detail": "Verification status can only be 'Verified' if there is at least one verification document."},
                )

        if instance.verification_status is models.VerificationStatus.PENDING.value and instance.verifier is None and verifier is not None:
            serializer.save(
                status=models.Status.NEW.value,
                verification_status=models.VerificationStatus.ASSIGNED.value,
                reviewer=None,
                verifier=verifier,
            )

        # TODO: Check if the other fields are being updated
        if status is models.Status.NEW.value:
            serializer.save(status=models.Status.NEW.value,
                            verification_status=models.VerificationStatus.PENDING.value,
                            reviewer=None,
                            verifier=None)

        serializer.save()


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows employees to be viewed or edited.
    """
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]


class VerificationDocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows verification documents to be viewed or edited.
    """
    queryset = VerificationDocument.objects.all()
    serializer_class = serializers.VerificationDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows roles to be viewed or edited.
    """
    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleSerializer
    permission_classes = [permissions.IsAuthenticated]
