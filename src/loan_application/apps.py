from django.apps import AppConfig


class LoanApplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'loan_application'

    def ready(self) -> None:
        import loan_application.signals as _
        return super().ready()
