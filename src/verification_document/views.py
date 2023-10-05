from rest_framework import viewsets, permissions
from api import serializers
from verification_document.models import VerificationDocument


class VerificationDocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows verification documents to be viewed or edited.
    """
    queryset = VerificationDocument.objects.all()
    serializer_class = serializers.VerificationDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
