from django.utils import timezone
from datetime import date

from edc_appointment.models import Appointment
from edc_constants.constants import YES, NO, POS, NEG, SCHEDULED

from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory
from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory
from microbiome.apps.mb_maternal.forms import RapidTestResultForm
from microbiome.apps.mb_maternal.tests.factories.maternal_visit_factory import MaternalVisitFactory

from .base_maternal_test_case import BaseMaternalTestCase


class TestRapidTestForm(BaseMaternalTestCase):

    def setUp(self):
        super(TestRapidTestForm, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject
        self.data = {
            'report_datetime': timezone.now(),
            'maternal_visit': None,
            'rapid_test_done': YES,
            'result_date': timezone.now(),
            'result': None,
        }

    def test_validate_rapid_test_done_no_result(self):
        self.maternal_consent.dob = date(2015, 12, 7)
        self.maternal_consent.save()
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_date=date.today(),
            rapid_test_result=NEG)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(appointment=appointment, reason=SCHEDULED)
        self.data['maternal_visit'] = maternal_visit.id
        rapid_form = RapidTestResultForm(data=self.data)
        self.assertIn("If a rapid test was processed, what is the test result?",
                      rapid_form.errors.get("__all__"))

    def test_validate_rapid_test_done_result(self):
        self.maternal_consent.dob = date(2015, 12, 7)
        self.maternal_consent.save()
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_date=date.today(),
            rapid_test_result=NEG)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(appointment=appointment, reason=SCHEDULED)
        self.data['maternal_visit'] = maternal_visit.id
        self.data['result'] = POS
        rapid_form = RapidTestResultForm(data=self.data)
        self.assertTrue(rapid_form.is_valid())

    def test_validate_rapid_test_done_no_result_date(self):
        self.maternal_consent.dob = date(2015, 12, 7)
        self.maternal_consent.save()
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(appointment=appointment, reason=SCHEDULED)
        self.data['maternal_visit'] = maternal_visit.id
        self.data['result_date'] = None
        self.data['result'] = POS
        rapid_form = RapidTestResultForm(data=self.data)
        self.assertIn(
            "If a rapid test was processed, what is the date of the rapid test?",
            rapid_form.errors.get("__all__"))

    def test_validate_rapid_test_not_done(self):
        self.maternal_consent.dob = date(2015, 12, 7)
        self.maternal_consent.save()
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(appointment=appointment, reason=SCHEDULED)
        self.data['maternal_visit'] = maternal_visit.id
        self.data['rapid_test_done'] = NO
        self.data['result_date'] = None
        self.data['result'] = None
        rapid_form = RapidTestResultForm(data=self.data)
        rapid_form.is_valid()
        self.assertTrue(rapid_form.is_valid())

    def test_validate_rapid_test_done_processed1(self):
        self.maternal_consent.dob = date(2015, 12, 7)
        self.maternal_consent.save()
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M')
        maternal_visit = MaternalVisitFactory(appointment=appointment, reason=SCHEDULED)
        result_date = date.today()
        self.data['maternal_visit'] = maternal_visit.id
        self.data['rapid_test_done'] = NO
        self.data['result_date'] = result_date
        self.data['result'] = None
        rapid_form = RapidTestResultForm(data=self.data)
        self.assertIn(
            'If a rapid test was not processed, please do not '
            'provide the result date. Got {}.'.format(result_date.strftime('%Y-%m-%d')),
            rapid_form.errors.get("__all__"))
