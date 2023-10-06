
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from loan_application.tests.utils import create_user, create_loan_application, create_employee
from loan_application.models import VerificationStatus
BASE_URL = reverse('verificationdocument-list')


class CreateLoanApplicationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_doesnt_allow_if_loan_application_is_not_assigned_to_verifier(self):
        loan_application = create_loan_application()
        request_body = self.create_body(loan_application)

        res = self.client.post(BASE_URL, request_body)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_allows_if_loan_application_is_assigned_to_verifier(self):
        loan_application = create_loan_application(
            verifier=create_employee(),
            verification_status=VerificationStatus.ASSIGNED.value
        )
        request_body = self.create_body(loan_application)

        res = self.client.post(BASE_URL, request_body)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def create_body(self, loan_application):
        request_body = {
            "document_type": 1,
            "file_path": "path/to/file.pdf",
            "loan_application": loan_application.id
        }

        return request_body
