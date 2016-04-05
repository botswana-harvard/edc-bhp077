from django.utils import timezone

from edc_appointment.models import Appointment
from edc_constants.choices import YES, NOT_APPLICABLE, POS
from edc_constants.constants import FAILED_ELIGIBILITY, LOST_VISIT, IN_PROGRESS, NEW_APPT

from microbiome.apps.mb_maternal.forms import MaternalVisitForm
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory

from .base_test_case import BaseTestCase
from .factories import PostnatalEnrollmentFactory, MaternalVisitFactory


class TestMaternalVisit(BaseTestCase):
    """Test eligibility of a mother for maternal visit."""

    def setUp(self):
        super(TestMaternalVisit, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject,
            study_site=self.study_site)
        self.registered_subject = self.maternal_consent.registered_subject
        self.postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            will_breastfeed=YES,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE)
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='2000M')
        self.data = {
            'appointment': self.appointment.id,
            'report_datetime': timezone.now(),
            'info_source': 'participant',
            'info_source_other': '',
            'reason': '',
            'reason_missed': '',
            'comments': '',
        }

    def test_missed_visit_no_reason(self):
        self.data['reason'] = 'missed'
        self.data['reason_missed'] = None
        form = MaternalVisitForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Provide reason visit was missed.', errors)

    def test_attended_visit_reason_missed_given(self):
        self.data['reason'] = 'scheduled'
        self.data['reason_missed'] = 'At work.'
        form = MaternalVisitForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Visit was not missed, do not provide reason visit was missed.', errors)

    def test_passed_enrollment_but_no_data_collection(self):
        """Test a participant who passed eligibility but no further data collection
        on visit report"""
        self.data['reason'] = FAILED_ELIGIBILITY
        form = MaternalVisitForm(data=self.data)
        self.assertIn(
            "Subject is eligible. Visit reason cannot be 'Failed Eligibility'",
            form.errors.get('__all__'))

    def test_appt_status_on_visit_reason_lost(self):
        """"Test that if the visit reason is lost then the appointment status will be 'In Progress'
        to allow data entry"""
        self.assertEqual(NEW_APPT, self.appointment.appt_status)
        MaternalVisitFactory(appointment=self.appointment, reason=LOST_VISIT)
        self.assertEqual(IN_PROGRESS, self.appointment.appt_status)

    def test_appt_status_on_completed_protocol(self):
        """"Test that if the visit reason is completed protocol then the appointment status will be 'In Progress'
        to allow data entry"""
        visit_code = ['2000M', '2010M', '2030M', '2060M', '2090M']
        for code in visit_code:
            appointment = Appointment.objects.get(
                registered_subject=self.registered_subject,
                visit_definition__code=code)
            MaternalVisitFactory(appointment=appointment)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='2120M')
        self.assertEqual(NEW_APPT, appointment.appt_status)
        MaternalVisitFactory(appointment=appointment, reason=LOST_VISIT)
        self.assertEqual(IN_PROGRESS, appointment.appt_status)
