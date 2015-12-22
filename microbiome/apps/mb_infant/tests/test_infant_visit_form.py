from datetime import date

from django.test import TestCase
from django.utils import timezone

from edc.subject.registration.models import RegisteredSubject
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc_appointment.models import Appointment
from edc_constants.constants import (
    YES, NO, POS, OFF_STUDY, ON_STUDY, DEATH_VISIT, LOST_VISIT, MISSED_VISIT,
    DEAD, ALIVE, SCHEDULED, NOT_APPLICABLE)

from microbiome.apps.mb.app_configuration.classes import MicrobiomeConfiguration
from microbiome.apps.mb.constants import INFANT
from microbiome.apps.mb_infant.forms import InfantVisitForm
from microbiome.apps.mb_infant.tests.factories import InfantBirthFactory
from microbiome.apps.mb_infant.visit_schedule import InfantBirthVisitSchedule
from microbiome.apps.mb_lab.lab_profiles import MaternalProfile, InfantProfile
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory
from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory
from microbiome.apps.mb_maternal.tests.factories.maternal_visit_factory import MaternalVisitFactory
from microbiome.apps.mb_maternal.visit_schedule import (
    AntenatalEnrollmentVisitSchedule, PostnatalEnrollmentVisitSchedule)


class TestInfantVisitForm(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
            site_lab_profiles.register(InfantProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        AntenatalEnrollmentVisitSchedule().build()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()
        InfantBirthVisitSchedule().build()

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

        registered_subject_infant = RegisteredSubject.objects.get(
            subject_type=INFANT,
            relative_identifier=registered_subject.subject_identifier)
        InfantBirthFactory(
            registered_subject=registered_subject_infant,
            maternal_labour_del=maternal_labour_del)
        self.appointment = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2000')

    def test_validate_reason_death_valid(self):
        data = {
            'is_present': NO,
            'reason': DEATH_VISIT,
            'survival_status': DEAD,
            'study_status': OFF_STUDY,
            'appointment': self.appointment.id,
            'info_source': 'other_doctor',
            'information_provider': 'MOTHER',
            'report_datetime': timezone.now(),
            'last_alive_date': date.today()}
        form = InfantVisitForm(data=data)
        self.assertTrue(form.is_valid())

    def test_validate_reason_death_not_valid(self):
        data = {
            'is_present': NO,
            'reason': DEATH_VISIT,
            'survival_status': ALIVE,
            'study_status': OFF_STUDY,
            'appointment': self.appointment.id,
            'info_source': 'other_doctor',
            'information_provider': 'MOTHER',
            'report_datetime': timezone.now()}
        form = InfantVisitForm(data=data)
        self.assertIn('A death is being reported. Select \'Deceased\' for survival status.',
                      form.errors.get('__all__'))

    def test_validate_reason_death_not_valid1(self):
        data = {
            'is_present': YES,
            'reason': OFF_STUDY,
            'survival_status': ALIVE,
            'study_status': ON_STUDY,
            'appointment': self.appointment.id,
            'info_source': 'other_doctor',
            'information_provider': 'MOTHER',
            'report_datetime': timezone.now()}
        form = InfantVisitForm(data=data)
        self.assertIn(
            "This is an Off Study or LFU visit. Select 'off study' for the infant's current study status.",
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
            "This is an Off Study or LFU visit. Select 'off study' for the infant's current study status.",
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
        self.assertTrue(form.is_valid())

    def test_validate_reason_missed_not_valid(self):
        data = {
            'is_present': NO,
            'reason': MISSED_VISIT,
            'survival_status': ALIVE,
            'study_status': ON_STUDY,
            'appointment': self.appointment.id,
            'info_source': 'other_doctor',
            'information_provider': 'MOTHER',
            'report_datetime': timezone.now()}
        form = InfantVisitForm(data=data)
        self.assertIn("Provide reason scheduled visit was missed.", form.errors.get('__all__'))

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
