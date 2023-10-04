
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from api import serializers
from loan_application.models import LoanApplication
from rest_framework import status
from rest_framework.test import APIClient
from customer.models import Customer
from employee.models import Employee, Role


LOAN_APPLICATIONS_URL = reverse('loanapplication-list')


def create_user(email='sample@example.com', password='passtest123'):
    return get_user_model().objects.create_user(username=email, email=email, password=password)


def create_role(**params):
    defaults = {
        "role_type": "Manager"
    }
    defaults.update(params)
    return Role.objects.create(**defaults)


def create_employee(**params):
    role = create_role()
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


class ListLoanApplicationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_should_list(self):
        create_loan_application(loan_amount=22)

        res = self.client.get(LOAN_APPLICATIONS_URL)

        loan_applications = LoanApplication.objects.all()
        serializer = serializers.LoanApplicationSerializer(
            loan_applications, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, serializer.data)
        # self.assertEqual(res.data['count'], 1)
        # self.assertEqual(res.data['next'], None)
        # self.assertEqual(res.data['previous'], None)
        self.assertEqual(res.data['results'], serializer.data)
