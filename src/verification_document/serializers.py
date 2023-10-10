from rest_framework import serializers
from verification_document.models import VerificationDocument


class VerificationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationDocument
        fields = '__all__'
