from django.test import TestCase

from ..models import MaternalScreening
from .factories import MaternalScreeningFactory


class TestMaternalEligibilityPre(TestCase):

    def test_can_save_pre_eligibility(self):
        pre_eligibility = MaternalScreeningFactory()
        self.assertEqual(MaternalScreening.objects.all().count(), 1)
