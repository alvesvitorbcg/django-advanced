from django.db import models
from core.models import BaseModel, Person
from django.db import models


class Role(BaseModel):
    role_type = models.CharField(max_length=100)

    def __str__(self):
        return self.role_type


class Employee(Person):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    user = models.OneToOneField(
        'auth.User', on_delete=models.CASCADE, null=True, blank=True)
