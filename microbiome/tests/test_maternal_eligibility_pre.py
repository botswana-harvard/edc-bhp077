from django.test import TestCase

from ..models import MaternalEligibilityPre
from .factories import MaternalEligibilityPreFactory


class TestMaternalEligibilityPre(TestCase):

    def test_can_save_pre_eligibility(self):
        pre_eligibility = MaternalEligibilityPreFactory()
        self.assertEqual(MaternalEligibilityPre.objects.all().count(), 1)
