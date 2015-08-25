from datetime import timedelta
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from microbiome.tests.factories.infant_birth_factory import InfantBirthFactory


class InfantModelTests(TestCase):

    def test_infantbirth_min_value(self):
        infant_birth = InfantBirthFactory()
        infant_birth.birth_order = 0
        self.assertRaises(ValidationError, infant_birth.full_clean)

    def test_infantbirth_max_value(self):
        infant_birth = InfantBirthFactory()
        infant_birth.birth_order = 5
        self.assertRaises(ValidationError, infant_birth.full_clean)

    def test_infantbirth_dob_not_future(self):
        infant_birth = InfantBirthFactory()
        infant_birth.dob = timezone.now().date() + timedelta(days=5)
        self.assertRaises(ValidationError, infant_birth.full_clean)
