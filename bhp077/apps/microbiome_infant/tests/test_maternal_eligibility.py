from datetime import date, timedelta
from django.test import TestCase
from django.utils import timezone
from edc_constants.constants import POS, YES, NO, NOT_APPLICABLE, NEG

from ..constants import (
    PENDING_BIRTH, HIV_INFECTED_COHORT, HIV_UNIFECTED_COHORT,
    NOT_ENROLLED, CESAREAN, PENDING_INFANT_RESULT)
from ..models import InfantEligibility, MaternalEligibility

from .factories import MaternalEligibilityFactory


class TestMaternalEligibilityPost(TestCase):

    def test_pending_birth_enrollment_status(self):
        options = {'currently_pregnant': YES}
        pre_eligibility = MaternalEligibilityFactory(**options)
        self.assertEqual(pre_eligibility.enrollment_status, PENDING_BIRTH)

    def test_not_enrolled_chronic_disease(self):
        options = {
            'currently_pregnant': NO,
            'disease': 'tuberculosis'
        }
        pre_eligibility = MaternalEligibilityFactory(**options)
        self.assertEqual(pre_eligibility.enrollment_status, NOT_ENROLLED)

    def test_not_enrolled_gestation(self):
        options = {
            'currently_pregnant': NO,
            'weeks_of_gestation': 35
        }
        pre_eligibility = MaternalEligibilityFactory(**options)
        self.assertEqual(pre_eligibility.enrollment_status, NOT_ENROLLED)

    def test_not_enrolled_postnatal_days(self):
        options = {
            'currently_pregnant': NO,
            'days_post_natal': 4
        }
        pre_eligibility = MaternalEligibilityFactory(**options)
        self.assertEqual(pre_eligibility.enrollment_status, NOT_ENROLLED)

    def test_not_enrolled_type_of_birth(self):
        options = {
            'currently_pregnant': NO,
            'type_of_birth': CESAREAN
        }
        pre_eligibility = MaternalEligibilityFactory(**options)
        self.assertEqual(pre_eligibility.enrollment_status, NOT_ENROLLED)

    def test_not_enrolled_live_infants(self):
        options = {
            'currently_pregnant': NO,
            'live_infants': 0
        }
        pre_eligibility = MaternalEligibilityFactory(**options)
        self.assertEqual(pre_eligibility.enrollment_status, NOT_ENROLLED)

    def test_not_enrolled_not_on_haart(self):
        options = {
            'currently_pregnant': NO,
            'live_infants': 1,
            'verbal_hiv_status': POS,
            'evidence_pos_hiv_status': YES,
            'haart_during_preg': NO
        }
        pre_eligibility = MaternalEligibilityFactory(**options)
        self.assertEqual(pre_eligibility.enrollment_status, NOT_ENROLLED)

    def test_not_enrolled_wrong_haart_drug(self):
        options = {
            'currently_pregnant': NO,
            'live_infants': 1,
            'verbal_hiv_status': POS,
            'evidence_pos_hiv_status': YES,
            'haart_during_preg': YES,
            'drug_during_preg': NOT_APPLICABLE
        }
        pre_eligibility = MaternalEligibilityFactory(**options)
        self.assertEqual(pre_eligibility.enrollment_status, NOT_ENROLLED)

    def test_not_enrolled_not_on_haart_long_enough(self):
        options = {
            'currently_pregnant': NO,
            'live_infants': 1,
            'verbal_hiv_status': POS,
            'days_post_natal': 1,
            'evidence_pos_hiv_status': YES,
            'haart_during_preg': YES,
            'haart_start_date': date.today() - timedelta(days=35),  # 5 weeks
            'drug_during_preg': 'Atripla'
        }
        pre_eligibility = MaternalEligibilityFactory(**options)
        self.assertEqual(pre_eligibility.enrollment_status, NOT_ENROLLED)

    def test_enrollment_pending_infant_result(self):
        options = {
            'currently_pregnant': NO,
            'live_infants': 1,
            'verbal_hiv_status': POS,
            'days_post_natal': 1,
            'evidence_pos_hiv_status': YES,
            'haart_during_preg': YES,
            'haart_start_date': date.today() - timedelta(days=49),  # 7 weeks
            'drug_during_preg': 'Atripla'
        }
        pre_eligibility = MaternalEligibilityFactory(**options)
        self.assertEqual(InfantEligibility.objects.all().count(), 1)
        self.assertEqual(pre_eligibility.enrollment_status, PENDING_INFANT_RESULT)

    def test_not_enrolled_infant_infected(self):
        options = {
            'currently_pregnant': NO,
            'live_infants': 1,
            'verbal_hiv_status': POS,
            'days_post_natal': 1,
            'evidence_pos_hiv_status': YES,
            'haart_during_preg': YES,
            'haart_start_date': date.today() - timedelta(days=49),  # 7 weeks
            'drug_during_preg': 'Atripla'
        }
        pre_eligibility = MaternalEligibilityFactory(**options)
        self.assertEqual(InfantEligibility.objects.all().count(), 1)
        self.assertEqual(pre_eligibility.enrollment_status, PENDING_INFANT_RESULT)
        # Make infant HIV +ve
        infant_eligibility = InfantEligibility.objects.get(maternal_eligibility_post=pre_eligibility)
        infant_eligibility.report_datetime = timezone.now()
        infant_eligibility.infant_hiv_result = POS
        infant_eligibility.save()
        pre_eligibility.save()
        # Re-evaluate enrollment with an HIV +ve infant
        pre_eligibility = MaternalEligibility.objects.get(id=pre_eligibility.id)
        self.assertEqual(pre_eligibility.enrollment_status, NOT_ENROLLED)

    def test_enrolled_in_hiv_infected_cohot(self):
        options = {
            'currently_pregnant': NO,
            'live_infants': 1,
            'verbal_hiv_status': POS,
            'days_post_natal': 1,
            'evidence_pos_hiv_status': YES,
            'haart_during_preg': YES,
            'haart_start_date': date.today() - timedelta(days=49),  # 7 weeks
            'drug_during_preg': 'Atripla'
        }
        pre_eligibility = MaternalEligibilityFactory(**options)
        self.assertEqual(InfantEligibility.objects.all().count(), 1)
        self.assertEqual(pre_eligibility.enrollment_status, PENDING_INFANT_RESULT)
        # Make infant HIV +ve
        infant_eligibility = InfantEligibility.objects.get(maternal_eligibility_post=pre_eligibility)
        infant_eligibility.report_datetime = timezone.now()
        infant_eligibility.infant_hiv_result = NEG
        infant_eligibility.save()
        pre_eligibility.save()
        # Re-evaluate enrollment with an HIV +ve infant
        pre_eligibility = MaternalEligibility.objects.get(id=pre_eligibility.id)
        self.assertEqual(pre_eligibility.enrollment_status, HIV_INFECTED_COHORT)

    def test_enrolled_in_hiv_uninfected_cohot(self):
        options = {
            'currently_pregnant': NO,
            'live_infants': 1,
            'verbal_hiv_status': NEG,
            'rapid_test_result': NEG
        }
        pre_eligibility = MaternalEligibilityFactory(**options)
        self.assertEqual(pre_eligibility.enrollment_status, HIV_UNIFECTED_COHORT)
