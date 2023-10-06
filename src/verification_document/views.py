from rest_framework import viewsets, permissions
from api import serializers
from verification_document.models import VerificationDocument
from loan_application.models import VerificationStatus, LoanApplication
from rest_framework.serializers import ValidationError


class VerificationDocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows verification documents to be viewed or edited.
    """
    queryset = VerificationDocument.objects.all()
    serializer_class = serializers.VerificationDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        loan_application = serializer.validated_data['loan_application']
        if loan_application.verification_status != VerificationStatus.ASSIGNED.value:
            raise ValidationError(
                {"detail": "Verification status must be 'Assigned' before a verification document can be created."},
            )
        else:
            serializer.save()
