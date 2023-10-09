from django.test import TestCase
from employee.models import Roles
from loan_application.tests.utils import create_employee, create_user
from verification_document.views import IsUserVerifierOrReviewer


class IsUserVerifierOrReviewerPermissionTest(TestCase):
    def setUp(self):
        self.permission = IsUserVerifierOrReviewer()
        self.request = self.client.get('/')

    def test_allow_if_user_is_verifier(self):
        verifier = create_employee(role_type=Roles.VERIFIER.name)
        self.request.user = verifier.user

        self.assertTrue(self.permission.has_permission(self.request, None))

    def test_allow_if_user_is_reviewer(self):
        reviewer = create_employee(role_type=Roles.REVIEWER.name)
        self.request.user = reviewer.user

        self.assertTrue(self.permission.has_permission(self.request, None))

    def test_not_allow_if_user_is_manager(self):
        manager = create_employee(role_type=Roles.MANAGER.name)
        self.request.user = manager.user

        self.assertFalse(self.permission.has_permission(self.request, None))

    def test_not_allow_if_user_is_not_employee_or_superuser(self):
        self.request.user = create_user(is_superuser=False)

        self.assertFalse(self.permission.has_permission(self.request, None))

    def test_allow_if_user_is_superuser(self):
        self.request.user = create_user(is_superuser=True)

        self.assertTrue(self.permission.has_permission(self.request, None))
