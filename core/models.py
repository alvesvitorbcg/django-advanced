from django.db import models


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
