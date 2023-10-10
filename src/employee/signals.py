from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from employee.models import Employee


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
