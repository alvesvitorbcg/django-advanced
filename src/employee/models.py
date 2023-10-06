from django.db import models
from core.models import BaseModel, Person
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Role(BaseModel):
    role_type = models.CharField(max_length=100)

    def __str__(self):
        return self.role_type


class Employee(Person):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    user = models.OneToOneField(
        'auth.User', on_delete=models.CASCADE, null=True, blank=True)


@receiver(post_save, sender=Employee)
def create_user_for_employee(sender, instance, created, **kwargs):
    if created:
        username = f"{instance.last_name[0]}{instance.first_name}{instance.id}"
        password = "changeme"
        email = f"{username}@nbfc.com"
        user = User.objects.create_user(
            username=username, password=password, email=email)
        instance.user = user
        instance.save()
