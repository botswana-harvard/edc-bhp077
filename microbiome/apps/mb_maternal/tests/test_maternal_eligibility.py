from django.test import TestCase

from bhp077.apps.microbiome_maternal.tests.factories import MaternalEligibilityFactory


class TestMaternalEligibility(TestCase):
    """Test eligibility of a mother."""

    def test_eligibility_for_correct_age(self):
        """Test eligibility of a mother with the right age."""
        options = {'age_in_years': 26}
        pre_eligibility = MaternalEligibilityFactory(**options)
        self.assertTrue(pre_eligibility.is_eligible)

    def test_eligibility_for_under_age(self):
        """Test eligibility of a mother with under age."""
        options = {'age_in_years': 17}
        pre_eligibility = MaternalEligibilityFactory(**options)
        self.assertFalse(pre_eligibility.is_eligible)

    def test_eligibility_for_over_age(self):
        """Test eligibility of a mother with over age."""
        options = {'age_in_years': 51}
        pre_eligibility = MaternalEligibilityFactory(**options)
        self.assertFalse(pre_eligibility.is_eligible)

    def test_eligibility_who_has_omang(self):
        """Test eligibility of a mother with an Omang."""
        options = {'has_omang': 'Yes'}
        pre_eligibility = MaternalEligibilityFactory(**options)
        self.assertTrue(pre_eligibility.is_eligible)

    def test_eligibility_who_has_no_omang(self):
        """Test eligibility of a mother with no Omang."""
        options = {'has_omang': 'No'}
        pre_eligibility = MaternalEligibilityFactory(**options)
        self.assertFalse(pre_eligibility.is_eligible)
