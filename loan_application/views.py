from rest_framework import viewsets, permissions, serializers as rest_serializers
from api import serializers
from loan_application.models import LoanApplication, Status, VerificationStatus
from verification_document.models import VerificationDocument


def is_result_status(status):
    return status is Status.APPROVED.value or status is Status.REJECTED.value


def is_assigned(verification_status):
    return verification_status == VerificationStatus.ASSIGNED.value


def is_verified(verification_status):
    return verification_status == VerificationStatus.VERIFIED.value


def is_verification_result_status(verification_status):
    return verification_status == VerificationStatus.VERIFIED.value or verification_status == VerificationStatus.FAILED.value


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
            verification_documents = VerificationDocument.objects.filter(
                loan_application=instance)

            if len(verification_documents) == 0:
                raise rest_serializers.ValidationError(
                    {"detail": "Verification status can only be 'Verified' if there is at least one verification document."},
                )

        if instance.verification_status is VerificationStatus.PENDING.value and instance.verifier is None and verifier is not None:
            serializer.save(
                status=Status.NEW.value,
                verification_status=VerificationStatus.ASSIGNED.value,
                reviewer=None,
                verifier=verifier,
            )

        # TODO: Check if the other fields are being updated
        if status is Status.NEW.value:
            serializer.save(status=Status.NEW.value,
                            verification_status=VerificationStatus.PENDING.value,
                            reviewer=None,
                            verifier=None)

        serializer.save()
