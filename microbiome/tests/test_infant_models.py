from django.test import TestCase
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

from ..models import InfantCongenitalAnomalies

from .factories import InfantBirthFactory, InfantBirthArvFactory, InfantBirthCnsAbnItemFactory, InfantVisitFactory


class InfantModelTests(TestCase):

    def test_infantbirth_min_value(self):
        infant_birth = InfantBirthFactory()
        infant_birth.birth_order = 0
        self.assertRaises(ValidationError, infant_birth.full_clean)

    def test_infantbirth_max_value(self):
        infant_birth = InfantBirthFactory()
        infant_birth.birth_order = 5
        self.assertRaises(ValidationError, infant_birth.full_clean)

    def test_infant_birth_order(self):
        infant_birth = InfantBirthFactory()
        infant_birth.birth_order = 5
        with self.assertRaises(ValidationError):
            infant_birth.full_clean()

    def test_infant_dob(self):
        infant_dob = InfantBirthFactory()
        infant_dob.dob = timezone.now().date() + timedelta(days=1)
        with self.assertRaises(ValidationError):
            infant_dob.full_clean()

    def test_infant_birth_azt_dose_date(self):
        infant_arv = InfantBirthArvFactory()
        infant_arv.azt_dose_date = timezone.now() + timedelta(days=1)
        with self.assertRaises(ValidationError):
            infant_arv.full_clean()

    def test_infant_nvp_dose_date(self):
        infant_nvp = InfantBirthArvFactory()
        infant_nvp.nvp_dose_date = timezone.now() + timedelta(days=1)
        with self.assertRaises(ValidationError):
            infant_nvp.full_clean()

    def test_cns_abn_item_date_not_future(self):
        infant = InfantCongenitalAnomalies.objects.create(infant_visit=InfantVisitFactory())
        basecns_item = InfantBirthCnsAbnItemFactory(congenital_anomalies=infant)
        basecns_item.report_datetime = timezone.now() + timedelta(days=1)
        with self.assertRaises(ValidationError):
            basecns_item.full_clean()

    def test_cns_abn_date_before_study_start(self):
        infant = InfantCongenitalAnomalies.objects.create(infant_visit=InfantVisitFactory())
        basecns_item = InfantBirthCnsAbnItemFactory(congenital_anomalies=infant)
        settings.STUDY_OPEN_DATETIME = timezone.now()
        basecns_item.report_datetime = timezone.now() - timedelta(days=1)
        with self.assertRaises(ValidationError):
            basecns_item.full_clean()
