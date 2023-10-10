from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from loan_application.tests.utils import create_user, create_loan_application

LOAN_APPLICATIONS_HISTORY_URL = reverse('loanapplicationhistory-list')


class CreateLoanApplicationHistory(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_create_loan_application_history_when_loan_application_is_created_and_updated(self):
        old_loan_amount = 1
        new_loan_amount = old_loan_amount + 1

        loan_application = create_loan_application(
            reviewer=None, verifier=None, loan_amount=old_loan_amount)

        loan_application.loan_amount = new_loan_amount
        loan_application.save()

        res = self.client.get(LOAN_APPLICATIONS_HISTORY_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        loan_application_history = sorted(
            res.data['results'], key=lambda x: x['id'], reverse=False)

        self.assertEqual(res.data['count'], 2)
        self.assertEqual(len(loan_application_history), 2)

        for index, history in enumerate(loan_application_history):
            if index == 0:
                self.assertEqual(history['loan_amount'], old_loan_amount)
            else:
                self.assertEqual(history['loan_amount'], new_loan_amount)

            self.assertEqual(history['status'], loan_application.status)

            self.assertEqual(history['verification_status'],
                             loan_application.verification_status)

            self.assertIsNone(history['reviewer'])
            self.assertEqual(history['manager'], loan_application.manager.id)
            self.assertIsNone(history['verifier'])
            self.assertEqual(history['customer'], loan_application.customer.id)
