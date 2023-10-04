from django.db import models
from core.models import Person


class Customer(Person):
    # TODO: verify how to define a class that inhertis from another class and doesnt define anything else
    def __str__(self):
        return self.first_name
