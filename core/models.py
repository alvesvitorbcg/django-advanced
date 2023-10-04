from django.db import models
from enum import Enum


class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Person(BaseModel):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, default=None)
    last_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        abstract = True


class Customer(Person):
    # TODO: verify how to define a class that inhertis from another class and doesnt define anything else
    def __str__(self):
        return self.first_name


class Role(BaseModel):
    role_type = models.CharField(max_length=100)

    def __str__(self):
        return self.role_type


class Employee(Person):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)


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


class VerificationDocument(BaseModel):
    document_type = models.IntegerField()
    loan_application = models.ForeignKey(
        LoanApplication, on_delete=models.SET_NULL, null=True, blank=True)
    file_path = models.CharField(max_length=100)
