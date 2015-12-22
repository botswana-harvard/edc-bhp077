from __future__ import print_function

from django.utils import timezone

from edc.core.bhp_variables.tests.factories.study_site_factory import StudySiteFactory
from edc_appointment.models import Appointment
from edc_constants.choices import YES, NO, POS, NOT_APPLICABLE

from microbiome.apps.mb_maternal.forms import MaternalArvPregForm, MaternalArvForm

from .base_maternal_test_case import BaseMaternalTestCase
from .factories import (PostnatalEnrollmentFactory, MaternalVisitFactory,
                        MaternalEligibilityFactory, MaternalConsentFactory)


class TestMaternalArvPreg(BaseMaternalTestCase):
    """Test eligibility of a mother for ARV Preg."""

    def setUp(self):
        super(TestMaternalArvPreg, self).setUp()
        study_site = StudySiteFactory(site_code='10', site_name='Gabs')
        maternal_eligibility = MaternalEligibilityFactory()
        maternal_consent = MaternalConsentFactory(
            registered_subject=maternal_eligibility.registered_subject,
            study_site=study_site)
        registered_subject = maternal_consent.registered_subject
        self.postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            will_breastfeed=YES,
        )
        self.appointment = Appointment.objects.get(registered_subject=registered_subject,
                                                   visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.data = {
            'maternal_visit': self.maternal_visit.id,
            'report_datetime': timezone.now(),
            'took_arv': YES,
            'is_interrupt': NO,
            'interrupt': 'N/A',
            'interrupt_other': '',
            'comment': '',
        }

    def test_valid_regimen_but_no_arv(self):
        """Assert that Enrollment shows participant on valid_regimen but now says
        did not take arv"""
        self.data['took_arv'] = NO
        self.postnatal_enrollment.valid_regimen_duration = YES
        self.postnatal_enrollment.save()
        form = MaternalArvPregForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            "At PNT you indicated that the participant has been on regimen for period of time. "
            "But now you indicated that the participant did not take ARVs. "
            "Please Correct.", errors)

    def test_medication_interrupted(self):
        """Assert that ARV indicated as interrupted, then reason expected"""
        self.data['is_interrupt'] = YES
        form = MaternalArvPregForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You indicated that ARVs were interrupted during pregnancy. '
                      'Please provide a reason', errors)

    def test_no_interruption_reason_given(self):
        """Assert that ARV indicated as not interrupted, then reason not expected"""
        self.data['interrupt'] = 'FORGOT'
        form = MaternalArvPregForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You indicated that ARVs were NOT interrupted during pregnancy. '
                      'You cannot provide a reason.', errors)

    def test_took_arv(self):
        """Assert arv taken but none listed"""
        form = MaternalArvPregForm(data=self.data)
        self.assertIn(
            "You indicated that participant started ARV(s) during this "
            "pregnancy. Please list them on 'Maternal ARV' table", form.errors.get('__all__'))

    def test_start_stop_date(self):
        """Assert you cannot put a stop date that is before the start date"""
        self.data['arv_code'] = '3TC'
        self.data['start_date'] = timezone.now().date()
        self.data['stop_date'] = timezone.now().date() - timezone.timedelta(days=1)
        form = MaternalArvForm(data=self.data)
        self.assertIn(
            'Your stop date of {} is prior to start date of {}. '
            'Please correct'.format(
                self.data['stop_date'], self.data['start_date']), form.errors.get('__all__'))
