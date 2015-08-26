from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.test import TestCase

from edc_registration.models import RegisteredSubject

from ..choices import (PENDING_BIRTH, PENDING_INFANT_RESULT, HIV_INFECTED_COHOT, HIV_UNIFECTED_COHOT,
                       NOT_ENROLLED, VAGINAL, CESAREAN, POS, YES, NOT_APPLICABLE)
from .factories import MaternalEligibilityPostFactory


class TestMaternalEligibilityPost(TestCase):

    def test_pending_birth_enrollment_status(self):
        options = {'currently_pregnant': 'Yes'}
        pre_eligibility = MaternalEligibilityPostFactory(**options)
        self.assertEqual(pre_eligibility.enrollment_status, PENDING_BIRTH)

    def test_not_enrolled_chronic_disease(self):
        options = {
            'currently_pregnant': 'No',
            'disease': 'tuberculosis'
        }
        pre_eligibility = MaternalEligibilityPostFactory(**options)
        self.assertEqual(pre_eligibility.enrollment_status, NOT_ENROLLED)

    def test_not_enrolled_gestation(self):
        options = {
            'currently_pregnant': 'No',
            'weeks_of_gestation': 35
        }
        pre_eligibility = MaternalEligibilityPostFactory(**options)
        self.assertEqual(pre_eligibility.enrollment_status, NOT_ENROLLED)

    def test_not_enrolled_postnatal_days(self):
        options = {
            'currently_pregnant': 'No',
            'days_post_natal': 4
        }
        pre_eligibility = MaternalEligibilityPostFactory(**options)
        self.assertEqual(pre_eligibility.enrollment_status, NOT_ENROLLED)

    def test_not_enrolled_type_of_birth(self):
        options = {
            'currently_pregnant': 'No',
            'type_of_birth': CESAREAN
        }
        pre_eligibility = MaternalEligibilityPostFactory(**options)
        self.assertEqual(pre_eligibility.enrollment_status, NOT_ENROLLED)
