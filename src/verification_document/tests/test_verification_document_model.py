from django.test import TestCase
from loan_application.tests.utils import create_loan_application, create_verification_document
from verification_document.models import VerificationDocument


class VerificationDocumentModelTests(TestCase):
    def test_verification_document_str(self):
        loan_application = create_loan_application()

        verification_document = create_verification_document(
            loan_application=loan_application)

        expected = f'{verification_document.id}_LA:{loan_application}'
        self.assertEqual(str(verification_document), expected)
