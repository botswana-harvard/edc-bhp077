from django.test import TestCase
from django.core.exceptions import ValidationError

from .factories import MaternalEligibilityPreFactory, SubjectConsentFactory


class TestConsentProcess(TestCase):
    
    def test_saving_consent(self):
        pre_eligibility = MaternalEligibilityPreFactory(currently_pregnant='pregnant')
        self.assertTrue(pre_eligibility.is_eligible) 
        subject_consent = SubjectConsentFactory(maternal_eligibility_pre=pre_eligibility)

    def test_saving_consent_with_failed_eligibility(self):
        pre_eligibility = MaternalEligibilityPreFactory(currently_pregnant='pregnant')
        pre_eligibility.citizen = 'No'
        self.assertFalse(pre_eligibility.is_eligible)
        with self.assertRaises(ValidationError):
            subject_consent = SubjectConsentFactory(maternal_eligibility_pre=pre_eligibility)