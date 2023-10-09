from django.contrib.auth import get_user_model

from loan_application.models import LoanApplication
from customer.models import Customer
from employee.models import Employee, Role, Roles
from verification_document.models import VerificationDocument


def create_user(email='sample@example.com', password='passtest123', is_superuser=False):
    return get_user_model().objects.create_user(username=email, email=email, password=password, is_superuser=is_superuser)


def create_role(**params):
    defaults = {
        "role_type": Roles.MANAGER.name
    }
    defaults.update(params)
    return Role.objects.create(**defaults)


def create_verification_document(loan_application, **params):
    defaults = {
        "document_type": 1,
        "file_path": "path/to/file.pdf",
        "loan_application": loan_application
    }
    defaults.update(params)
    return VerificationDocument.objects.create(**defaults)


def create_employee(role_type=Roles.MANAGER.name, **params):
    role = create_role(role_type=role_type)
    defaults = {
        "first_name": "Maria",
        "middle_name": "Mac",
        "last_name": "Miller",
        "mobile": "31996145581",
        "role": role
    }
    defaults.update(params)
    return Employee.objects.create(**defaults)


def create_customer(**params):
    defaults = {
        "first_name": "Carol",
        "middle_name": "Chrysler",
        "last_name": "Cane",
        "mobile": "31996145581"
    }
    defaults.update(params)
    return Customer.objects.create(**defaults)


def create_loan_application(**params):
    customer = create_customer()
    employee = create_employee()
    defaults = {
        "date_created": "2023-10-04T20:18:43.325567Z",
        "date_updated": "2023-10-04T20:18:43.325592Z",
        "status": 0,
        "verification_status": 0,
        "loan_amount": 1,
        "reviewer": None,
        "manager": employee,
        "customer": customer,
        "verifier": None
    }
    defaults.update(params)
    loan_application = LoanApplication.objects.create(**defaults)
    return loan_application
