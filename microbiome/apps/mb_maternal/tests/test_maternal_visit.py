from django.utils import timezone

from edc_appointment.models import Appointment
from edc_constants.choices import YES, NOT_APPLICABLE, POS
from edc_constants.constants import NO_FURTHER_DATA_COLLECTION

from microbiome.apps.mb_maternal.forms import MaternalVisitForm
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory

from .base_maternal_test_case import BaseMaternalTestCase
from .factories import PostnatalEnrollmentFactory, MaternalVisitFactory


class TestMaternalVisit(BaseMaternalTestCase):
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
        self.assertIn('You indicated that the visit was missed. Please provide a reason why '
                      'it was missed.', errors)

    def test_attended_visit_reason_missed_given(self):
        self.data['reason'] = 'scheduled'
        self.data['reason_missed'] = 'At work.'
        form = MaternalVisitForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You indicated that the visit was NOT missed, yet you provided a reason '
                      'why it was missed. Please correct.', errors)

    def test_passed_enrollment_but_no_data_collection(self):
        """Test a participant who passed eligibility but no further data collection
        on visit report"""
        self.data['reason'] = NO_FURTHER_DATA_COLLECTION
        form = MaternalVisitForm(data=self.data)
        self.assertIn(
            "Subject is eligible. Visit reason cannot be 'No further data collection'",
            form.errors.get('__all__'))
