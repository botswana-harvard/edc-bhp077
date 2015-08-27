from datetime import datetime, date, timedelta
from django.test import TestCase

from ..choices import (PENDING_BIRTH, PENDING_INFANT_RESULT, HIV_INFECTED_COHOT, HIV_UNIFECTED_COHOT, NEG,
                       NOT_ENROLLED, CESAREAN, POS, YES, NO, NOT_APPLICABLE, PENDING_INFANT_RESULT)
from .factories import MaternalEligibilityPostFactory
from ..models import InfantEligibility, MaternalEligibilityPost

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

    def test_not_enrolled_live_infants(self):
        options = {
            'currently_pregnant': 'No',
            'live_infants': 0
        }
        pre_eligibility = MaternalEligibilityPostFactory(**options)
        self.assertEqual(pre_eligibility.enrollment_status, NOT_ENROLLED)

    def test_not_enrolled_not_on_haart(self):
        options = {
            'currently_pregnant': 'No',
            'live_infants': 1,
            'verbal_hiv_status': POS,
            'evidence_pos_hiv_status': YES,
            'haart_during_preg': NO
        }
        pre_eligibility = MaternalEligibilityPostFactory(**options)
        self.assertEqual(pre_eligibility.enrollment_status, NOT_ENROLLED)

    def test_not_enrolled_wrong_haart_drug(self):
        options = {
            'currently_pregnant': 'No',
            'live_infants': 1,
            'verbal_hiv_status': POS,
            'evidence_pos_hiv_status': YES,
            'haart_during_preg': YES,
            'drug_during_preg': NOT_APPLICABLE
        }
        pre_eligibility = MaternalEligibilityPostFactory(**options)
        self.assertEqual(pre_eligibility.enrollment_status, NOT_ENROLLED)

    def test_not_enrolled_not_on_haart_long_enough(self):
        options = {
            'currently_pregnant': 'No',
            'live_infants': 1,
            'verbal_hiv_status': POS,
            'days_post_natal': 1,
            'evidence_pos_hiv_status': YES,
            'haart_during_preg': YES,
            'haart_start_date': date.today() - timedelta(days=35),  # 5 weeks
            'drug_during_preg': 'Atripla'
        }
        pre_eligibility = MaternalEligibilityPostFactory(**options)
        self.assertEqual(pre_eligibility.enrollment_status, NOT_ENROLLED)

    def test_enrollment_pending_infant_result(self):
        options = {
            'currently_pregnant': 'No',
            'live_infants': 1,
            'verbal_hiv_status': POS,
            'days_post_natal': 1,
            'evidence_pos_hiv_status': YES,
            'haart_during_preg': YES,
            'haart_start_date': date.today() - timedelta(days=49),  # 7 weeks
            'drug_during_preg': 'Atripla'
        }
        pre_eligibility = MaternalEligibilityPostFactory(**options)
        self.assertEqual(InfantEligibility.objects.all().count(), 1)
        self.assertEqual(pre_eligibility.enrollment_status, PENDING_INFANT_RESULT)

    def test_not_enrolled_infant_infected(self):
        options = {
            'currently_pregnant': 'No',
            'live_infants': 1,
            'verbal_hiv_status': POS,
            'days_post_natal': 1,
            'evidence_pos_hiv_status': YES,
            'haart_during_preg': YES,
            'haart_start_date': date.today() - timedelta(days=49),  # 7 weeks
            'drug_during_preg': 'Atripla'
        }
        pre_eligibility = MaternalEligibilityPostFactory(**options)
        self.assertEqual(InfantEligibility.objects.all().count(), 1)
        self.assertEqual(pre_eligibility.enrollment_status, PENDING_INFANT_RESULT)
        # Make infant HIV +ve
        infant_eligibility = InfantEligibility.objects.get(maternal_eligibility_post=pre_eligibility)
        infant_eligibility.report_datetime = datetime.now()
        infant_eligibility.infant_hiv_result = POS
        infant_eligibility.save()
        pre_eligibility.save()
        # Re-evaluate enrollment with an HIV +ve infant
        pre_eligibility = MaternalEligibilityPost.objects.get(id=pre_eligibility.id)
        self.assertEqual(pre_eligibility.enrollment_status, NOT_ENROLLED)

    def test_enrolled_in_hiv_infected_cohot(self):
        options = {
            'currently_pregnant': 'No',
            'live_infants': 1,
            'verbal_hiv_status': POS,
            'days_post_natal': 1,
            'evidence_pos_hiv_status': YES,
            'haart_during_preg': YES,
            'haart_start_date': date.today() - timedelta(days=49),  # 7 weeks
            'drug_during_preg': 'Atripla'
        }
        pre_eligibility = MaternalEligibilityPostFactory(**options)
        self.assertEqual(InfantEligibility.objects.all().count(), 1)
        self.assertEqual(pre_eligibility.enrollment_status, PENDING_INFANT_RESULT)
        # Make infant HIV +ve
        infant_eligibility = InfantEligibility.objects.get(maternal_eligibility_post=pre_eligibility)
        infant_eligibility.report_datetime = datetime.now()
        infant_eligibility.infant_hiv_result = NEG
        infant_eligibility.save()
        pre_eligibility.save()
        # Re-evaluate enrollment with an HIV +ve infant
        pre_eligibility = MaternalEligibilityPost.objects.get(id=pre_eligibility.id)
        self.assertEqual(pre_eligibility.enrollment_status, HIV_INFECTED_COHOT)

    def test_enrolled_in_hiv_uninfected_cohot(self):
        options = {
            'currently_pregnant': 'No',
            'live_infants': 1,
            'verbal_hiv_status': NEG,
            'rapid_test_result': NEG
        }
        pre_eligibility = MaternalEligibilityPostFactory(**options)
        self.assertEqual(pre_eligibility.enrollment_status, HIV_UNIFECTED_COHOT)
