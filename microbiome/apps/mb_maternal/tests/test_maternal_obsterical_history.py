from django.utils import timezone

from edc_appointment.models import Appointment
from edc_constants.constants import YES, NEG, SCHEDULED

from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory
from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory
from microbiome.apps.mb_maternal.forms import MaternalObstericalHistoryForm

from .factories import MaternalVisitFactory

from .base_test_case import BaseTestCase


class TestMaternalObstericalHistoryForm(BaseTestCase):

    def setUp(self):
        super(TestMaternalObstericalHistoryForm, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=appointment, reason=SCHEDULED)

        self.data = {
            'report_datetime': timezone.now(),
            'maternal_visit': self.maternal_visit.id,
            'prev_pregnancies': 2,
            'pregs_24wks_or_more': 1,
            'lost_before_24wks': 1,
            'lost_after_24wks': 1,
            'live_children': 1,
            'children_died_b4_5yrs': 1
        }

    def test_maternal_obsterical_history_form_valid(self):
        mob = MaternalObstericalHistoryForm(data=self.data)
        self.assertTrue(mob.is_valid())

    def test_maternal_obsterical_history_form_valid1(self):
        self.data = {
            'report_datetime': timezone.now(),
            'maternal_visit': self.maternal_visit.id,
            'prev_pregnancies': 1,
            'pregs_24wks_or_more': 1,
            'lost_before_24wks': 0,
            'lost_after_24wks': 0,
            'live_children': 1,
            'children_died_b4_5yrs': 0
        }
        mob = MaternalObstericalHistoryForm(data=self.data)
        self.assertTrue(mob.is_valid())

    def test_maternal_obsterical_history_children_died_b4_5yrs_invalid(self):
        self.data['children_died_b4_5yrs'] = -1
        mob = MaternalObstericalHistoryForm(data=self.data)
        self.assertFalse(mob.is_valid())

    def test_maternal_obsterical_history_children_died_b4_5yrs_valid(self):
        self.data = {
            'report_datetime': timezone.now(),
            'maternal_visit': self.maternal_visit.id,
            'prev_pregnancies': 1,
            'pregs_24wks_or_more': 1,
            'lost_before_24wks': 0,
            'lost_after_24wks': 0,
            'live_children': 1,
            'children_died_b4_5yrs': 1
        }
        mob = MaternalObstericalHistoryForm(data=self.data)
        self.assertTrue(mob.is_valid())

    def test_maternal_obsterical_history_live_children_invalid(self):
        self.data['live_children'] = -1
        mob = MaternalObstericalHistoryForm(data=self.data)
        self.assertFalse(mob.is_valid())

    def test_maternal_obsterical_history_live_children_valid(self):
        self.data['live_children'] = 2
        mob = MaternalObstericalHistoryForm(data=self.data)
        self.assertTrue(mob.is_valid())

    def test_maternal_obsterical_history_pregs_24wks_or_more_invalid(self):
        self.data['pregs_24wks_or_more'] = -1
        self.data['lost_after_24wks'] = 2
        self.data['children_died_b4_5yrs'] = 2
        mob = MaternalObstericalHistoryForm(data=self.data)
        self.assertFalse(mob.is_valid())

    def test_maternal_obsterical_history_pregs_24wks_or_more_valid(self):
        self.data['pregs_24wks_or_more'] = 1
        self.data['lost_after_24wks'] = 1
        self.data['children_died_b4_5yrs'] = 1
        mob = MaternalObstericalHistoryForm(data=self.data)
        self.assertTrue(mob.is_valid())

    def test_zero_previous_pregnancies(self):
        self.data['prev_pregnancies'] = -1
        self.data['pregs_24wks_or_more'] = 1
        mob = MaternalObstericalHistoryForm(data=self.data)
        self.assertFalse(mob.is_valid())

    def test_prev_pregnancies_zero(self):
        self.data['prev_pregnancies'] = 0
        self.data['pregs_24wks_or_more'] = 1
        self.data['lost_before_24wks'] = 1
        self.data['lost_after_24wks'] = 3
        mob = MaternalObstericalHistoryForm(data=self.data)
        self.assertIn(u"You indicated previous pregancies were 0. Number of pregnancies at or after 24 weeks,number "
                      "of living children,number of children died after 5 year be greater than all be zero.",
                      mob.errors.get('__all__'))

    def test_prev_pregnancies_zero_1(self):
        self.data['prev_pregnancies'] = 1
        self.data['pregs_24wks_or_more'] = 0
        self.data['lost_before_24wks'] = 0
        self.data['lost_after_24wks'] = 0
        mob = MaternalObstericalHistoryForm(data=self.data)
        self.assertIn("You indicated previous pregancies were 1. Number of pregnancies at or after 24 weeks,"
                      "number of living children,number of children died after 5 year CANNOT all be zero.",
                      mob.errors.get('__all__'))

    def test_preg24wks_grt_prev_preg(self):
        self.data['prev_pregnancies'] = 2
        self.data['pregs_24wks_or_more'] = 3
        mob = MaternalObstericalHistoryForm(data=self.data)
        self.assertIn(
            "Number of pregnancies carried at least 24 weeks cannot be greater than previous pregnancies.",
            mob.errors.get('__all__'))

    def test_lost_before_24wks_grt_prev_preg(self):
        self.data['prev_pregnancies'] = 2
        self.data['lost_before_24wks'] = 3
        mob = MaternalObstericalHistoryForm(data=self.data)
        self.assertIn(
            "Number of pregnancies lost before 24 weeks cannot be greater than previous pregnancies.",
            mob.errors.get('__all__'))

    def test_lost_after_24wks_grt_prev_preg(self):
        self.data['prev_pregnancies'] = 2
        self.data['pregs_24wks_or_more'] = 1
        self.data['lost_before_24wks'] = 1
        self.data['lost_after_24wks'] = 3
        mob = MaternalObstericalHistoryForm(data=self.data)
        self.assertIn("Number of pregnancies lost at or after 24 weeks gestation cannot be greater "
                      "than number of previous pregnancies or number of pregnancies at least 24 weeks.",
                      mob.errors.get('__all__'))

    def test_pregs_24wks_or_more_plus_lost_before_24wks_grt_prev_pregnancies(self):
        self.data['prev_pregnancies'] = 3
        self.data['pregs_24wks_or_more'] = 1
        self.data['lost_before_24wks'] = 1
        self.data['lost_after_24wks'] = 1
        mob = MaternalObstericalHistoryForm(data=self.data)
        self.assertIn("The sum of Number of pregnancies at least 24 weeks and "
                      "number of pregnancies lost before 24 weeks gestation. must be equal to "
                      "number of previous pregnancies for this participant.", mob.errors.get('__all__'))
