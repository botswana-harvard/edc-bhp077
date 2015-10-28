from datetime import timedelta

from django.utils import timezone
from django.core.exceptions import ValidationError
from django.test import TestCase

from .factories import MaternalLabourDelFactory


class TestMicrobiomeMaternal(TestCase):

    def test_maternal_labour_del(self):
        maternal_labour = MaternalLabourDelFactory()
        maternal_labour.delivery_datetime = timezone.now() + timedelta(days=1)
        with self.assertRaises(ValidationError):
            maternal_labour.full_clean()
