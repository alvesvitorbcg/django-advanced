
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from api import serializers, models
from rest_framework import status
from rest_framework.test import APIClient


LOAN_APPLICATIONS_URL = reverse('loanapplication-list')
LOAN_APPLICATION_MOCK_OBJECT = {
    "loan_amount": 1,
    "manager": 2,
    "customer": 1,
}


def create_user(email='sample@example.com', password='passtest123'):
    return get_user_model().objects.create_user(username=email, email=email, password=password)


def create_loan_application(user, **params):
    defaults = LOAN_APPLICATION_MOCK_OBJECT
    defaults.update(params)
    print(f'{user}')
    # loan_application = serializers.LoanApplicationSerializer().create(defaults)
    loan_application = models.LoanApplication.objects.create(
        user=user, **defaults)
    return loan_application


class LoanApplicationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_loan_applications(self):
        create_loan_application(self.user, loan_amount=22)
        create_loan_application(self.user, loan_amount=33)

        res = self.client.get(LOAN_APPLICATIONS_URL)

        # ingredients = Ingredient.objects.all().order_by('-name')
        # serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, serializer.data)
