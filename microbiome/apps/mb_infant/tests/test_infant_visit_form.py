from datetime import date
from dateutil.relativedelta import relativedelta

from django.utils import timezone

from edc_registration.models import RegisteredSubject
from edc_appointment.models import Appointment
from edc_constants.constants import (
    YES, NO, POS, OFF_STUDY, ON_STUDY, LOST_VISIT, MISSED_VISIT,
    DEAD, ALIVE, SCHEDULED, NOT_APPLICABLE, IN_PROGRESS, NEW_APPT)

from microbiome.apps.mb.constants import INFANT
from microbiome.apps.mb_infant.forms import InfantVisitForm
from microbiome.apps.mb_infant.tests.factories import InfantBirthFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory
from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory
from microbiome.apps.mb_maternal.tests.factories.maternal_visit_factory import MaternalVisitFactory

from .base_test_case import BaseTestCase
from .factories import InfantVisitFactory


class TestInfantVisitForm(BaseTestCase):

    def setUp(self):
        super(TestInfantVisitForm, self).setUp()
        maternal_eligibility = MaternalEligibilityFactory()
        maternal_consent = MaternalConsentFactory(registered_subject=maternal_eligibility.registered_subject)
        registered_subject = maternal_consent.registered_subject

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            rapid_test_result=None,
            rapid_test_date=None)
        self.assertTrue(postnatal_enrollment.is_eligible)

        appointment = Appointment.objects.get(
            registered_subject=registered_subject,
            visit_definition__code='1000M')
        MaternalVisitFactory(appointment=appointment)
        appointment = Appointment.objects.get(
            registered_subject=registered_subject, visit_definition__code='2000M')
        maternal_visit = MaternalVisitFactory(appointment=appointment)
        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)

        self.registered_subject_infant = RegisteredSubject.objects.get(
            subject_type=INFANT,
            relative_identifier=registered_subject.subject_identifier)
        InfantBirthFactory(
            registered_subject=self.registered_subject_infant,
            maternal_labour_del=maternal_labour_del)
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject_infant,
            visit_definition__code='2000')

    def test_appt_status_on_visit_reason_lost(self):
        """"Test that if the visit reason is lost then the appointment status will be 'In Progress'
        to allow data entry"""
        self.assertEqual(NEW_APPT, self.appointment.appt_status)
        InfantVisitFactory(appointment=self.appointment, reason=LOST_VISIT)
        self.assertEqual(IN_PROGRESS, self.appointment.appt_status)

    def test_appt_status_on_completed_protocol(self):
        """"Test that if the visit reason is completed protocol then the appointment status will be 'In Progress'
        to allow data entry"""
        visit_code = ['2000', '2010', '2030', '2060', '2090']
        for code in visit_code:
            appointment = Appointment.objects.get(
                registered_subject=self.registered_subject_infant,
                visit_definition__code=code)
            InfantVisitFactory(appointment=appointment)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject_infant,
            visit_definition__code='2120')
        self.assertEqual(NEW_APPT, appointment.appt_status)
        InfantVisitFactory(appointment=appointment, reason=LOST_VISIT)
        self.assertEqual(IN_PROGRESS, appointment.appt_status)

    def test_validate_reason_death_valid(self):
        data = {
            'is_present': NO,
            'reason': SCHEDULED,
            'survival_status': DEAD,
            'study_status': OFF_STUDY,
            'appointment': self.appointment.id,
            'info_source': 'other_doctor',
            'information_provider': 'MOTHER',
            'report_datetime': timezone.now(),
            'last_alive_date': date.today()}
        form = InfantVisitForm(data=data)
        self.assertTrue(form.is_valid)

    def test_validate_reason_death_not_valid1(self):
        data = {
            'is_present': NO,
            'reason': LOST_VISIT,
            'survival_status': ALIVE,
            'study_status': ON_STUDY,
            'appointment': self.appointment.id,
            'info_source': 'other_doctor',
            'information_provider': 'MOTHER',
            'report_datetime': timezone.now(),
            'last_alive_date': date.today() - relativedelta(weeks=4)}
        form = InfantVisitForm(data=data)
        self.assertIn(
            "The infant is reported as lost to follow-up. Select 'off study' for the infant's current study status.",
            form.errors.get('__all__'))

    def test_validate_reason_lost_and_completed(self):
        data = {
            'is_present': NO,
            'reason': LOST_VISIT,
            'survival_status': DEAD,
            'study_status': ON_STUDY,
            'appointment': self.appointment.id,
            'info_source': 'other_doctor',
            'information_provider': 'MOTHER',
            'report_datetime': timezone.now(),
            'last_alive_date': date.today()}
        form = InfantVisitForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "The infant is reported as lost to follow-up. Select 'off study' for the infant's current study status.",
            form.errors.get('__all__'))

    def test_validate_reason_missed_valid(self):
        data = {
            'is_present': NO,
            'reason': MISSED_VISIT,
            'survival_status': ALIVE,
            'study_status': ON_STUDY,
            'appointment': self.appointment.id,
            'information_provider': 'MOTHER',
            'report_datetime': timezone.now(),
            'reason_missed': 'I was in the cattle post.',
            'last_alive_date': date.today()}
        form = InfantVisitForm(data=data)
        self.assertTrue(form.is_valid)

    def test_validate_reason_missed_not_valid(self):
        data = {
            'is_present': NO,
            'reason': MISSED_VISIT,
            'survival_status': ALIVE,
            'study_status': ON_STUDY,
            'appointment': self.appointment.id,
            'info_source': 'other_doctor',
            'information_provider': 'MOTHER',
            'report_datetime': timezone.now(),
            'last_alive_date': date.today()}
        form = InfantVisitForm(data=data)
        self.assertIn("Provide reason visit was missed.", form.errors.get('__all__'))

    def test_validate_survival_status(self):
        data = {
            'is_present': YES,
            'reason': SCHEDULED,
            'survival_status': ALIVE,
            'study_status': ON_STUDY,
            'appointment': self.appointment.id,
            'info_source': 'other_doctor',
            'information_provider': 'MOTHER',
            'report_datetime': timezone.now(),
        }
        form = InfantVisitForm(data=data)
        self.assertIn('Provide date infant last known alive.', form.errors.get('__all__'))
