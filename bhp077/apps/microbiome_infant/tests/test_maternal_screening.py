from django.test import TestCase

from ..models import MaternalScreening

from .factories import MaternalScreeningFactory


class TestMaternalEligibilityPre(TestCase):

    def test_can_save(self):
        MaternalScreeningFactory()
        self.assertEqual(MaternalScreening.objects.all().count(), 1)
