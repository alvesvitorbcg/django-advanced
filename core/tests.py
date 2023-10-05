from django.test import TestCase
from core.models import Person


class PersonTests(TestCase):
    class PersonConcrete(Person):
        pass

    def test_str(self):
        person = self.PersonConcrete(
            first_name='John', last_name='Doe', mobile='1234567890')
        self.assertEqual(str(person), 'John Doe')
