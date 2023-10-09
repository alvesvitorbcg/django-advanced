
from django.test import TestCase
from django.urls import reverse
from api import serializers

from rest_framework import status
from employee.models import Roles
from rest_framework.test import APIClient
from loan_application.constants import Errors
from loan_application.tests.utils import create_user, create_employee, create_loan_application

LOAN_APPLICATIONS_URL = reverse('loanapplication-list')


class ListLoanApplicationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(is_superuser=True)
        self.client.force_authenticate(self.user)

    def test_list_all_if_user_is_admin(self):
        LOAN_APPLICATIONS_COUNT = 3
        loan_applications = []

        for _ in range(LOAN_APPLICATIONS_COUNT):
            loan_applications.append(create_loan_application())

        loan_applications = sorted(serializers.LoanApplicationSerializer(
            loan_applications, many=True).data, key=lambda x: x['id'])

        res = self.client.get(LOAN_APPLICATIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data['count'], LOAN_APPLICATIONS_COUNT)
        self.assertEqual(len(res.data['results']), LOAN_APPLICATIONS_COUNT)
        self.assertEqual(
            sorted(res.data['results'], key=lambda x: x['id']), loan_applications)

    def test_returns_only_own_loan_applications_for_manager(self):
        authenticated_manager = create_employee(role_type=Roles.MANAGER.name)
        self.client.force_authenticate(authenticated_manager.user)

        create_loan_application()

        loan_application_assigned_to_user = create_loan_application(
            manager=authenticated_manager)

        loan_application_assigned_to_user = serializers.LoanApplicationSerializer(
            loan_application_assigned_to_user, many=False).data

        res = self.client.get(LOAN_APPLICATIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data['count'], 1)
        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'][0],
                         loan_application_assigned_to_user)

    def test_returns_only_own_loan_applications_for_reviewer(self):
        authenticated_reviewer = create_employee(role_type=Roles.REVIEWER.name)
        self.client.force_authenticate(authenticated_reviewer.user)

        create_loan_application()

        loan_application_assigned_to_user = create_loan_application(
            reviewer=authenticated_reviewer)

        loan_application_assigned_to_user = serializers.LoanApplicationSerializer(
            loan_application_assigned_to_user, many=False).data

        res = self.client.get(LOAN_APPLICATIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data['count'], 1)
        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'][0],
                         loan_application_assigned_to_user)

    def test_returns_only_own_loan_applications_for_verifier(self):
        authenticated_verifier = create_employee(role_type=Roles.VERIFIER.name)
        self.client.force_authenticate(authenticated_verifier.user)

        create_loan_application()
        loan_application_assigned_to_user = create_loan_application(
            verifier=authenticated_verifier)

        loan_application_assigned_to_user = serializers.LoanApplicationSerializer(
            loan_application_assigned_to_user, many=False).data

        res = self.client.get(LOAN_APPLICATIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data['count'], 1)
        self.assertEqual(len(res.data['results']), 1)
        self.assertEqual(res.data['results'][0],
                         loan_application_assigned_to_user)

    def test_returns_error_if_user_is_not_employee_or_admin(self):
        self.client.force_authenticate(create_user(
            email="notsuperuser@nbfc.com", is_superuser=False))

        res = self.client.get(LOAN_APPLICATIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data[0], Errors.USER_IS_NOT_EMPLOYEE)

    def test_returns_error_if_user_has_unknown_employee_role(self):
        self.client.force_authenticate(
            create_employee(role_type='UNKNOWN').user)
        res = self.client.get(LOAN_APPLICATIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(res.data[0], Errors.ROLE_NOT_VALID)
