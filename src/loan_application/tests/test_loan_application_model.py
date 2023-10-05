from django.test import TestCase
from loan_application.tests.utils import create_loan_application, create_customer


class LoanApplicationModelTests(TestCase):
    def test_loan_application(self):
        customer = create_customer()
        loan_application = create_loan_application(customer=customer)
        expected = f'{loan_application.id}_{customer}_{loan_application.date_created}'
        self.assertEqual(str(loan_application), expected)
