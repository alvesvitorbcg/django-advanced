from django.db import models
from core.models import BaseModel
from loan_application.models import LoanApplication


class VerificationDocument(BaseModel):
    document_type = models.IntegerField()
    loan_application = models.ForeignKey(
        LoanApplication, on_delete=models.SET_NULL, null=True, blank=True)
    file_path = models.CharField(max_length=100)
