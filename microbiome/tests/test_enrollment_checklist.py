from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.test import TestCase

from .factories import EligibilityChecklistFactory


class TestEnrollmentChecklist(TestCase):

    def test_cannot_save_future_dob(self):
        checklist = EligibilityChecklistFactory()
        checklist.dob = timezone.now().date() + timedelta(days=1)
        with self.assertRaises(ValidationError):
            checklist.save()
        
    def test_date_before_study_start(self):
        checklist = EligibilityChecklistFactory()
        settings.STUDY_OPEN_DATETIME = timezone.now().date()
        checklist.report_datetime = timezone.now() - timedelta(days=1)
        with self.assertRaises(ValidationError):
            checklist.save()
    
    def test_report_datetime_not_future(self):
        checklist = EligibilityChecklistFactory()
        checklist.report_datetime = timezone.now() + timedelta(days=1)
        with self.assertRaises(ValidationError):
            checklist.save()