from django.dispatch import receiver
from django.db.models.signals import post_save
from loan_application.models import LoanApplication, LoanApplicationHistory


@receiver(post_save, sender=LoanApplication)
def create_loan_application_history(sender, instance, **kwargs):
    history_instance = LoanApplicationHistory(loan_application=instance)
    history_instance.__dict__.update(instance.__dict__)
    history_instance.id = None
    history_instance.save()
