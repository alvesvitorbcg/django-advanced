from rest_framework import viewsets, permissions
from api import serializers
from verification_document.constants import Errors
from verification_document.models import VerificationDocument
from loan_application.enums import VerificationStatus
from rest_framework.serializers import ValidationError
from rest_framework.permissions import BasePermission
from employee.models import Employee
from employee.enums import Roles


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
        permissions.IsAuthenticated]

    def perform_create(self, serializer):
        loan_application = serializer.validated_data['loan_application']
        if loan_application.verification_status != VerificationStatus.ASSIGNED.value:
            raise ValidationError(
                Errors.CREATING_DOCUMENT_IS_ONLY_ALLOWED_FOR_ASSIGNED_LOAN_APPLICATIONS)
        else:
            serializer.save()

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        if self.action == 'create':
            permission_classes.append(IsUserVerifierOrReviewer)

        return [permission() for permission in permission_classes]
