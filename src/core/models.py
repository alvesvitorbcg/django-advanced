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
