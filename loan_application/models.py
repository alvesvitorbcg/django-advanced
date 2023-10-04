from enum import Enum
from django.db import models
from core.models import BaseModel, Customer, Employee


class Status(Enum):
    NEW = 0
    APPROVED = 1
    REJECTED = 2


class VerificationStatus(Enum):
    PENDING = 0
    ASSIGNED = 1
    VERIFIED = 2
    FAILED = 3


class LoanApplication(BaseModel):
    class Meta:
        ordering = ['-id']

    status = models.IntegerField(default=Status.NEW.value)
    verification_status = models.IntegerField(
        default=VerificationStatus.PENDING.value)
    reviewer = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewer')
    manager = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='manager')
    loan_amount = models.IntegerField()
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='customer')
    verifier = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='verifier')

    @property
    def has_verifier(self):
        return self.verifier is not None

    @property
    def has_reviewer(self):
        return self.reviewer is not None

    @property
    def is_verification_status_verified(self):
        return self.verification_status is VerificationStatus.VERIFIED.value


class LoanApplicationHistory(LoanApplication):
    loan_application = models.ForeignKey(
        LoanApplication, on_delete=models.CASCADE, null=True, blank=True, related_name='loan_application_history')
