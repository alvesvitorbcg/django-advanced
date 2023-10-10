from rest_framework import viewsets, permissions
from api.serializers import LoanApplicationHistorySerializer, LoanApplicationSerializer
from employee.enums import Roles
from loan_application.constants import Errors
from loan_application.models import LoanApplication, LoanApplicationHistory
from loan_application.enums import Status, VerificationStatus
from verification_document.models import VerificationDocument
from employee.models import Employee
from rest_framework.exceptions import ValidationError


def is_result_status(status):
    return status is Status.APPROVED.value or status is Status.REJECTED.value


def is_assigned(verification_status):
    return verification_status == VerificationStatus.ASSIGNED.value


def is_verified(verification_status):
    return verification_status == VerificationStatus.VERIFIED.value


def is_verification_result_status(verification_status):
    return verification_status == VerificationStatus.VERIFIED.value or verification_status == VerificationStatus.FAILED.value


class LoanApplicationViewSet(viewsets.ModelViewSet):
    queryset = LoanApplication.objects.all()
    serializer_class = LoanApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if (user.is_superuser):
            return self.queryset

        employee = Employee.objects.filter(user=user).first()

        if employee is None:
            raise ValidationError(Errors.USER_IS_NOT_EMPLOYEE)

        if employee.role.role_type == Roles.VERIFIER.name:
            return self.queryset.filter(verifier=employee)

        elif employee.role.role_type == Roles.REVIEWER.name:
            return self.queryset.filter(reviewer=employee)

        if employee.role.role_type == Roles.MANAGER.name:
            return self.queryset.filter(manager=employee)
        else:
            raise ValidationError(Errors.ROLE_NOT_VALID)

    def perform_create(self, serializer):
        serializer.save(
            status=Status.NEW.value,
            verification_status=VerificationStatus.PENDING.value,
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
            raise ValidationError(
                Errors.VERIFICATION_STATUS_CANT_BE_ASSIGNED_WITHOUT_VERIFIER,
            )

        if is_verification_result_status(verification_status) and not instance.has_verifier:
            raise ValidationError(
                Errors.VERIFICATION_STATUS_CANT_BE_DECIDED_WITHOUT_VERIFIER,
            )

        if is_result_status(status) and (not instance.has_reviewer or not instance.has_verifier or not instance.is_verification_status_verified):
            raise ValidationError(
                Errors.STATUS_CANT_BE_DECIDED_WITHOUT_REVIEWER_VERIFIER_OR_VERIFIED_STATUS,
            )

        if reviewer is not None and not instance.has_reviewer and not instance.is_verification_status_verified:
            raise ValidationError(
                Errors.REVIEWER_CANT_BE_ASSIGNED_IF_NOT_VERIFIED,
            )

        if is_verified(verification_status):
            verification_documents = VerificationDocument.objects.filter(
                loan_application=instance)

            if len(verification_documents) == 0:
                raise ValidationError(
                    Errors.VERIFICATION_STATUS_CANT_BE_VERIFIED_WITHOUT_DOCUMENTS,
                )

        if instance.verification_status is VerificationStatus.PENDING.value and instance.verifier is None and verifier is not None:
            serializer.validated_data.update(
                status=Status.NEW.value,
                verification_status=VerificationStatus.ASSIGNED.value,
                reviewer=None,
                verifier=verifier,
            )

        if status is Status.NEW.value:
            serializer.validated_data.update(
                status=Status.NEW.value,
                verification_status=VerificationStatus.PENDING.value,
                reviewer=None,
                verifier=None,
            )

        serializer.save()


class LoanApplicationHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LoanApplicationHistory.objects.all()
    serializer_class = LoanApplicationHistorySerializer
