from django.test import TransactionTestCase
from django.core.exceptions import ValidationError

from microbiome.models import SubjectConsent

from .factories import MaternalEligibilityPreFactory, SubjectConsentFactory


class TestSubject(TransactionTestCase):

    def test_consent(self):
        subject_consent = SubjectConsent()
        print([f.name for f in subject_consent._meta.fields])

    def test_pre_eligibility_matches(self):
        pre_eligibility = MaternalEligibilityPreFactory()
        subject_consent = SubjectConsentFactory(maternal_eligibility_pre=pre_eligibility)
        self.assertTrue(subject_consent.matches_maternal_eligibility_pre(subject_consent, pre_eligibility))

    def test_pre_eligibility_matches_gender(self):
        pre_eligibility = MaternalEligibilityPreFactory()
        subject_consent = SubjectConsentFactory(maternal_eligibility_pre=pre_eligibility)
        pre_eligibility.gender = 'M'
        with self.assertRaises(ValidationError):
            subject_consent.matches_maternal_eligibility_pre(subject_consent, pre_eligibility)

#     def test_pre_eligibility_matches_age(self):
#         pre_eligibility = MaternalEligibilityPreFactory()
#         subject_consent = SubjectConsentFactory(maternal_eligibility_pre=pre_eligibility)
#         pre_eligibility.age_in_years = pre_eligibility.age_in_years - 1
#         with self.assertRaises(ValidationError):
#             subject_consent.matches_maternal_eligibility_pre(subject_consent, pre_eligibility)
