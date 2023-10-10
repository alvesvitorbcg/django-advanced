from django.test import TestCase
from loan_application.tests.utils import create_loan_application, create_customer
from loan_application.models import LoanApplicationHistory


class LoanApplicationModelTests(TestCase):
    def test_loan_application_str(self):
        customer = create_customer()
        loan_application = create_loan_application(customer=customer)
        expected = f'{loan_application.id}_{customer}'
        self.assertEqual(str(loan_application), expected)


class LoanApplicationHistoryModelTests(TestCase):
    def test_loan_application_history_str(self):
        customer = create_customer()
        loan_application = create_loan_application(customer=customer)
        loan_application_history = LoanApplicationHistory.objects.filter(
            loan_application=loan_application).first()
        expected = f'{loan_application_history.id}_LA:{loan_application.id}_{customer}'
        self.assertEqual(str(loan_application_history), expected)
