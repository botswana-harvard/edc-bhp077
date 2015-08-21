from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.test import TestCase

from .factories import MaternalEligibilityPreFactory


class TestMaternalEligibilityPre(TestCase):

    def test_cannot_save_future_dob(self):
        checklist = MaternalEligibilityPreFactory()
        checklist.dob = timezone.now().date() + timedelta(days=1)
        with self.assertRaises(ValidationError):
            checklist.full_clean()
        
    def test_date_before_study_start(self):
        checklist = MaternalEligibilityPreFactory()
        settings.STUDY_OPEN_DATETIME = timezone.now()
        checklist.report_datetime = timezone.now() - timedelta(days=1)
        with self.assertRaises(ValidationError):
            checklist.full_clean()
    
    def test_report_datetime_not_future(self):
        checklist = MaternalEligibilityPreFactory()
        checklist.report_datetime = timezone.now() + timedelta(days=1)
        with self.assertRaises(ValidationError):
            checklist.full_clean()