
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from api import serializers
from core import models
from rest_framework import status
from rest_framework.test import APIClient


LOAN_APPLICATIONS_URL = reverse('loanapplication-list')


def create_user(email='sample@example.com', password='passtest123'):
    return get_user_model().objects.create_user(username=email, email=email, password=password)


def create_role(**params):
    defaults = {
        "role_type": "Manager"
    }
    defaults.update(params)
    return models.Role.objects.create(**defaults)


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
    return models.Employee.objects.create(**defaults)


def create_customer(**params):
    defaults = {
        "first_name": "Carol",
        "middle_name": "Chrysler",
        "last_name": "Cane",
        "mobile": "31996145581"
    }
    defaults.update(params)
    return models.Customer.objects.create(**defaults)


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
    loan_application = models.LoanApplication.objects.create(**defaults)
    return loan_application


class CreateLoanApplicationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_enforces_default_values(self):
        request_body = self.create_body()

        res = self.client.post(LOAN_APPLICATIONS_URL, request_body)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(res.data['status'], models.Status.NEW.value)
        self.assertEqual(res.data['verification_status'],
                         models.VerificationStatus.PENDING.value)
        self.assertEqual(res.data['reviewer'], None)
        self.assertEqual(res.data['verifier'], None)

    def test_applies_permitted_inputs(self):
        request_body = self.create_body()

        res = self.client.post(LOAN_APPLICATIONS_URL, request_body)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['loan_amount'], request_body['loan_amount'])
        self.assertEqual(res.data['manager'], request_body['manager'])
        self.assertEqual(res.data['customer'], request_body['customer'])

    def test_persists_loan_application_in_database(self):
        request_body = self.create_body()

        res = self.client.post(LOAN_APPLICATIONS_URL, request_body)

        inserted_loan_application_object = models.LoanApplication.objects.filter(
            id=res.data['id']).first()

        inserted_loan_application = serializers.LoanApplicationSerializer(
            inserted_loan_application_object, many=False).data

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(res.data, inserted_loan_application,
                         "The response data should match the data persisted in the database")

    def create_body(self):
        customer = create_customer()
        employee = create_employee()

        request_body = {
            "status": 99,
            "verification_status": 99,
            "loan_amount": 31311,
            "manager": employee.id,
            "customer": customer.id,
            "reviewer": employee.id,
            "verifier": employee.id,
        }

        return request_body
