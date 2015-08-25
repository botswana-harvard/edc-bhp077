from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.test import TestCase

from edc_registration.models import RegisteredSubject

from .factories import MaternalEligibilityPreFactory


class TestMaternalEligibilityPre(TestCase):

    def test_creates_registered_subject(self):
        pre_eligibility = MaternalEligibilityPreFactory()
        self.assertEqual(RegisteredSubject.objects.filter(
            registration_identifier=pre_eligibility.internal_identifier).count(), 1)
        
    def test_passes_pre_eligibility_pregnant(self):
        pre_eligibility = MaternalEligibilityPreFactory(currently_pregnant='pregnant')
        self.assertTrue(pre_eligibility.is_eligible)
    
    def test_fails_pre_eligibility_pregnant(self):
        pre_eligibility = MaternalEligibilityPreFactory(currently_pregnant='pregnant', has_identity='No')
        self.assertFalse(pre_eligibility.is_eligible)
        
        pre_eligibility.has_identity = 'Yes'
        pre_eligibility.citizen = 'No'
        self.assertFalse(pre_eligibility.is_eligible)
        
        pre_eligibility.citizen = 'Yes'
        pre_eligibility.disease = 'tuberculosis'
        self.assertFalse(pre_eligibility.is_eligible)
    
    def test_passes_pre_eligibility_delivered(self):
        pre_eligibility = MaternalEligibilityPreFactory(currently_pregnant='delivered', pregnancy_weeks=38)
        self.assertTrue(pre_eligibility.is_eligible)
    
    def test_fails_pre_eligibility_delivered(self):
        pre_eligibility = MaternalEligibilityPreFactory(currently_pregnant='delivered', pregnancy_weeks=35)
        self.assertFalse(pre_eligibility.is_eligible)
    
    def test_fails_pre_eligibility_hiv_status(self):
        pre_eligibility = MaternalEligibilityPreFactory(currently_pregnant='pregnant')
        self.assertTrue(pre_eligibility.is_eligible)
        
        pre_eligibility.verbal_hiv_status = 'NEG'
        pre_eligibility.rapid_test_result = 'POS'
        self.assertFalse(pre_eligibility.is_eligible)
        
        pre_eligibility.verbal_hiv_status = 'NEG'
        pre_eligibility.rapid_test_result = 'NEG'
        self.assertTrue(pre_eligibility.is_eligible)