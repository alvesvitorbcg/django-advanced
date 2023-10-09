
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from loan_application.models import Status, VerificationStatus
from rest_framework.test import APIClient
from loan_application.tests.utils import create_user, create_employee, create_loan_application, create_verification_document

LOAN_APPLICATIONS_URL = reverse('loanapplication-list')


def detail_url(id):
    return reverse('loanapplication-detail', args=[id])


class UpdateReviewerLoanApplicationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(is_superuser=True)
        self.client.force_authenticate(self.user)

    def test_doesnt_allow_set_reviewer_if_verification_status_is_not_verified(self):
        loan_application = create_loan_application()
        loan_application.verifier = create_employee()
        loan_application.verification_status = VerificationStatus.FAILED.value
        loan_application.save()

        request_body = {
            "reviewer": create_employee().id
        }

        url = detail_url(loan_application.id)

        res = self.client.patch(url, request_body)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_allow_set_reviewer_if_verification_status_is_not_verified(self):
        loan_application = create_loan_application()
        loan_application.verifier = create_employee()
        loan_application.verification_status = VerificationStatus.VERIFIED.value
        loan_application.save()

        request_body = {
            "reviewer": create_employee().id
        }

        url = detail_url(loan_application.id)

        res = self.client.patch(url, request_body)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['reviewer'], request_body['reviewer'])


class UpdateStatusLoanApplicationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(is_superuser=True)
        self.client.force_authenticate(self.user)

    def test_doesnt_allow_set_status_approved_if_application_has_no_verifier(self):
        loan_application = create_loan_application()

        request_body = {
            "status": Status.APPROVED.value
        }

        url = detail_url(loan_application.id)

        res = self.client.patch(url, request_body)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_doesnt_allow_set_status_approved_if_application_has_no_reviewer(self):
        loan_application = create_loan_application()
        loan_application.verifier = create_employee()
        loan_application.verification_status = VerificationStatus.VERIFIED.value
        loan_application.save()

        request_body = {
            "status": Status.APPROVED.value
        }

        url = detail_url(loan_application.id)

        res = self.client.patch(url, request_body)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_doesnt_allow_set_status_approved_if_application_verification_status_is_not_verified(self):
        loan_application = create_loan_application()
        loan_application.verifier = create_employee()
        loan_application.reviewer = create_employee()
        loan_application.verification_status = VerificationStatus.FAILED.value
        loan_application.save()

        request_body = {
            "status": Status.APPROVED.value
        }

        url = detail_url(loan_application.id)

        res = self.client.patch(url, request_body)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_allows_set_status_approved_if_application_verification_status_is_verified_and_reviewer_assigned(self):
        loan_application = create_loan_application()
        loan_application.verifier = create_employee()
        loan_application.reviewer = create_employee()
        loan_application.verification_status = VerificationStatus.VERIFIED.value
        loan_application.save()

        request_body = {
            "status": Status.APPROVED.value
        }

        url = detail_url(loan_application.id)

        res = self.client.patch(url, request_body)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['status'], Status.APPROVED.value)

    def test_application_is_reset_initial_state_when_status_is_changed_to_new(self):
        loan_application = create_loan_application()
        loan_application.verifier = create_employee()
        loan_application.reviewer = create_employee()
        loan_application.verification_status = VerificationStatus.VERIFIED.value
        loan_application.status = Status.APPROVED.value
        loan_application.save()

        request_body = {
            "status": Status.NEW.value
        }

        url = detail_url(loan_application.id)

        res = self.client.patch(url, request_body)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['status'], Status.NEW.value)
        self.assertEqual(res.data['verification_status'],
                         VerificationStatus.PENDING.value)
        self.assertEqual(res.data['reviewer'], None)
        self.assertEqual(res.data['verifier'], None)


class UpdateVerificationStatusLoanApplicationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(is_superuser=True)
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

    def test_doesnt_allow_set_verification_status_to_failed_if_application_hadnt_been_assigned_to_verifier(self):
        loan_application = create_loan_application()

        request_body = {
            "verification_status": VerificationStatus.FAILED.value
        }

        url = detail_url(loan_application.id)

        res = self.client.patch(url, request_body)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_doesnt_allow_set_verification_status_to_verified_if_application_hadnt_been_assigned_to_verifier(self):
        loan_application = create_loan_application()

        request_body = {
            "verification_status": VerificationStatus.VERIFIED.value
        }

        url = detail_url(loan_application.id)

        res = self.client.patch(url, request_body)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_doesnt_allow_set_verification_status_to_verified_if_application_has_no_uploaded_verification_document(self):
        loan_application = create_loan_application()
        loan_application.verifier = create_employee()
        loan_application.verification_status = VerificationStatus.ASSIGNED.value
        loan_application.save()

        request_body = {
            "verification_status": VerificationStatus.VERIFIED.value
        }

        url = detail_url(loan_application.id)

        res = self.client.patch(url, request_body)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_allow_set_verification_status_to_verified_if_application_has_uploaded_verification_document(self):
        loan_application = create_loan_application()
        loan_application.verifier = create_employee()
        loan_application.verification_status = VerificationStatus.ASSIGNED.value
        loan_application.save()
        create_verification_document(
            loan_application)

        request_body = {
            "verification_status": VerificationStatus.VERIFIED.value
        }

        url = detail_url(loan_application.id)

        res = self.client.patch(url, request_body)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['verification_status'],
                         VerificationStatus.VERIFIED.value)

    def test_sets_verification_status_to_assigned_when_verifier_is_assigned_to_pending_application(self):
        loan_application = create_loan_application()
        loan_application.save()

        request_body = {
            "verifier": create_employee().id
        }

        url = detail_url(loan_application.id)

        res = self.client.patch(url, request_body)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['verification_status'],
                         VerificationStatus.ASSIGNED.value)
