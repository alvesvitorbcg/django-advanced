from django.db import models
from enum import Enum
# Create your models here.


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

    # @property
    # def role_id(self):
    #     if self.role:
    #         return self.role.id
    #     return None


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

    # @property
    # def reviewer_id(self):
    #     if self.reviewer:
    #         return self.reviewer.id
    #     return None

    # @property
    # def manager_id(self):
    #     if self.manager:
    #         return self.manager.id
    #     return None

    # @property
    # def customer_id(self):
    #     if self.customer:
    #         return self.customer.id
    #     return None

    # @property
    # def verifier_id(self):
    #     if self.verifier:
    #         return self.verifier.id
    #     return None


class VerificationDocument(BaseModel):
    document_type = models.IntegerField()
    loan_application = models.ForeignKey(
        LoanApplication, on_delete=models.SET_NULL, null=True, blank=True)
    file_path = models.CharField(max_length=100)

    # @property
    # def loan_application_id(self):
    #     if self.loan_application:
    #         return self.loan_application.id
    #     return None
