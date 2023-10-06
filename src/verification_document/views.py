from rest_framework import viewsets, permissions
from api import serializers
from verification_document.models import VerificationDocument
from loan_application.models import VerificationStatus, LoanApplication
from rest_framework.serializers import ValidationError
from rest_framework.permissions import BasePermission
from employee.models import Roles, Employee


class IsUserVerifierOrReviewer(BasePermission):
    """
    Allows access only for employees with Verifier role.
    """

    def has_permission(self, request, view):
        user = request.user
        if user.is_superuser:
            return True
        employee = Employee.objects.filter(user=user).first()
        if employee is None:
            return False
        if employee.role.role_type == Roles.VERIFIER.name or employee.role.role_type == Roles.REVIEWER.name:
            return True
        return False


class VerificationDocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows verification documents to be viewed or edited.
    """
    queryset = VerificationDocument.objects.all()
    serializer_class = serializers.VerificationDocumentSerializer
    permission_classes = [
        permissions.IsAuthenticated, IsUserVerifierOrReviewer]

    def perform_create(self, serializer):
        loan_application = serializer.validated_data['loan_application']
        if loan_application.verification_status != VerificationStatus.ASSIGNED.value:
            raise ValidationError(
                {"detail": "Verification status must be 'Assigned' before a verification document can be created."},
            )
        else:
            serializer.save()
