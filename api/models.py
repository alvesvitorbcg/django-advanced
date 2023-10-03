from django.db import models

# Create your models here.


class BaseModel(models.Model):
    id = models.IntegerField(primary_key=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Person(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Customer(Person):
    def __str__(self):
        return self.id


class Role(BaseModel):
    role = models.IntegerField()

    def __str__(self):
        return self.id


class Employee(Person):
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
