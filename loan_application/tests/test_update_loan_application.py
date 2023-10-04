
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from loan_application.models import VerificationStatus
from rest_framework.test import APIClient
from loan_application.tests.utils import create_user, create_employee, create_loan_application

LOAN_APPLICATIONS_URL = reverse('loanapplication-list')


def detail_url(id):
    return reverse('loanapplication-detail', args=[id])


class UpdateLoanApplicationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_doesnt_allow_set_verification_status_to_assigned_without_verifier(self):
        loan_application = create_loan_application()

        request_body = {
            "verification_status": VerificationStatus.ASSIGNED.value
        }

        url = detail_url(loan_application.id)

        res = self.client.patch(url, request_body)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_allow_set_verification_status_to_assigned_if_request_also_contains_verifier(self):
        loan_application = create_loan_application()

        request_body = {
            "verification_status": VerificationStatus.ASSIGNED.value,
            "verifier": create_employee().id
        }

        url = detail_url(loan_application.id)

        res = self.client.patch(url, request_body)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['verification_status'],
                         VerificationStatus.ASSIGNED.value)
        self.assertEqual(res.data['verifier'], request_body['verifier'])

    def test_allow_set_verification_status_to_assigned_if_application_had_been_assigned_to_verifier(self):
        loan_application = create_loan_application()
        employee = create_employee()
        loan_application.verifier = employee
        loan_application.save()

        request_body = {
            "verification_status": VerificationStatus.ASSIGNED.value
        }

        url = detail_url(loan_application.id)

        res = self.client.patch(url, request_body)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['verification_status'],
                         VerificationStatus.ASSIGNED.value)
        self.assertEqual(res.data['verifier'], employee.id)
