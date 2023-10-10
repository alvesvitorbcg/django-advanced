
from django.test import TestCase
from django.urls import reverse
from loan_application.serializers import LoanApplicationSerializer
from rest_framework import status
from loan_application.models import LoanApplication
from loan_application.enums import Status, VerificationStatus
from rest_framework.test import APIClient
from loan_application.tests.utils import create_user, create_employee, create_customer

LOAN_APPLICATIONS_URL = reverse('loanapplication-list')


class CreateLoanApplicationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_enforces_default_values(self):
        request_body = self.create_body()

        res = self.client.post(LOAN_APPLICATIONS_URL, request_body)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(res.data['status'], Status.NEW.value)
        self.assertEqual(res.data['verification_status'],
                         VerificationStatus.PENDING.value)
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

        inserted_loan_application_object = LoanApplication.objects.filter(
            id=res.data['id']).first()

        inserted_loan_application = LoanApplicationSerializer(
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
