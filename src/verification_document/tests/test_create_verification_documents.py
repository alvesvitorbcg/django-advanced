
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from loan_application.tests.utils import create_loan_application, create_employee
from loan_application.models import VerificationStatus
from employee.models import Roles

BASE_URL = reverse('verificationdocument-list')


class CreateVerficationDocumentsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.verifier = create_employee(
            role_type=Roles.VERIFIER.name)
        self.manager = create_employee(role_type=Roles.MANAGER.name)
        self.reviewer = create_employee(
            role_type=Roles.REVIEWER.name)

    def test_forbidden_if_user_is_manager(self):
        loan_application = create_loan_application()
        self.client.force_authenticate(self.manager.user)
        request_body = self.create_body(loan_application)

        res = self.client.post(BASE_URL, request_body)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_doesnt_allow_if_loan_application_is_not_assigned_to_verifier(self):
        loan_application = create_loan_application()
        self.client.force_authenticate(self.verifier.user)
        request_body = self.create_body(loan_application)

        res = self.client.post(BASE_URL, request_body)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_allows_if_loan_application_is_assigned_to_verifier_and_user_is_verifier(self):
        loan_application = create_loan_application(
            verifier=self.verifier,
            verification_status=VerificationStatus.ASSIGNED.value
        )
        self.client.force_authenticate(self.verifier.user)
        request_body = self.create_body(loan_application)

        res = self.client.post(BASE_URL, request_body)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_allows_if_loan_application_is_assigned_to_verifier_and_user_is_reviewer(self):
        loan_application = create_loan_application(
            reviewer=self.reviewer,
            verification_status=VerificationStatus.ASSIGNED.value
        )
        self.client.force_authenticate(self.reviewer.user)
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
