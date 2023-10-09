from django.test import TestCase
from employee.models import Role


class RoleTests(TestCase):
    def test_role(self):
        role_type = 'Manager'
        role = Role(role_type=role_type)
        self.assertEqual(str(role), role_type)
