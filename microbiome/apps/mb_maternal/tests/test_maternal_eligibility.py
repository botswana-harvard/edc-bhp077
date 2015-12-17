from django.test import TestCase

from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory
from edc_constants.constants import SCREENED
from edc.subject.registration.models.registered_subject import RegisteredSubject


class TestMaternalEligibility(TestCase):
    """Test eligibility of a mother."""

    def test_eligibility_for_correct_age(self):
        """Test eligibility of a mother with the right age."""
        options = {'age_in_years': 26}
        maternal_eligibility = MaternalEligibilityFactory(**options)
        self.assertTrue(maternal_eligibility.is_eligible)

    def test_eligibility_for_under_age(self):
        """Test eligibility of a mother with under age."""
        options = {'age_in_years': 17}
        maternal_eligibility = MaternalEligibilityFactory(**options)
        self.assertFalse(maternal_eligibility.is_eligible)

    def test_eligibility_for_over_age(self):
        """Test eligibility of a mother with over age."""
        options = {'age_in_years': 51}
        maternal_eligibility = MaternalEligibilityFactory(**options)
        self.assertFalse(maternal_eligibility.is_eligible)

    def test_eligibility_who_has_omang(self):
        """Test eligibility of a mother with an Omang."""
        options = {'has_omang': 'Yes'}
        maternal_eligibility = MaternalEligibilityFactory(**options)
        self.assertTrue(maternal_eligibility.is_eligible)

    def test_eligibility_who_has_no_omang(self):
        """Test eligibility of a mother with no Omang."""
        options = {'has_omang': 'No'}
        maternal_eligibility = MaternalEligibilityFactory(**options)
        self.assertFalse(maternal_eligibility.is_eligible)

    def test_updates_registered_subject_on_add(self):
        options = {'age_in_years': 26}
        self.assertEqual(RegisteredSubject.objects.all().count(), 0)
        maternal_eligibility = MaternalEligibilityFactory(**options)
        self.assertTrue(maternal_eligibility.is_eligible)
        registered_subject = RegisteredSubject.objects.get(pk=maternal_eligibility.registered_subject.pk)
        self.assertEquals(registered_subject.screening_datetime, maternal_eligibility.report_datetime)
        self.assertEquals(registered_subject.registration_status, SCREENED)

    def test_updates_registered_subject_on_edit(self):
        options = {'age_in_years': 26}
        self.assertEqual(RegisteredSubject.objects.all().count(), 0)
        maternal_eligibility = MaternalEligibilityFactory(**options)
        self.assertTrue(maternal_eligibility.is_eligible)
        maternal_eligibility.age_in_years = 27
        maternal_eligibility.save()
        registered_subject = RegisteredSubject.objects.get(screening_identifier=maternal_eligibility.eligibility_id)
        self.assertEquals(registered_subject.screening_age_in_years, 27)
        self.assertEquals(registered_subject.registration_status, SCREENED)
