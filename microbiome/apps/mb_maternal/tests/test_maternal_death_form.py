from django.test import TestCase
from django.utils import timezone

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc_constants.constants import YES, NO, NEG

from microbiome.apps.mb.app_configuration.classes import MicrobiomeConfiguration
from microbiome.apps.mb_maternal.forms import MaternalDeathReportForm

from microbiome.apps.mb_lab.lab_profiles import MaternalProfile
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory, MaternalVisitFactory
from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory
from microbiome.apps.mb_maternal.visit_schedule import PostnatalEnrollmentVisitSchedule
from edc.subject.registration.models.registered_subject import RegisteredSubject
from dateutil.relativedelta import relativedelta
from edc_death_report.models import DiagnosisCode, Cause
from edc_death_report.models.cause_category import CauseCategory
from edc_death_report.models.medical_responsibility import MedicalResponsibility
from edc_death_report.models.reason_hospitalized import ReasonHospitalized


class TestMaternalDeathReportForm(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()

        maternal_eligibility = MaternalEligibilityFactory()
        registered_subject = RegisteredSubject.objects.get(
            pk=maternal_eligibility.registered_subject.pk)
        self.maternal_consent = MaternalConsentFactory(registered_subject=registered_subject)
        self.registered_subject = RegisteredSubject.objects.get(pk=registered_subject.pk)
        self.assertEqual(self.registered_subject.registration_datetime,
                         self.maternal_consent.consent_datetime)

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        self.assertTrue(postnatal_enrollment.is_eligible)

        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='1000M')
        MaternalVisitFactory(appointment=appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        MaternalLabourDelFactory(maternal_visit=self.maternal_visit)
        self.data = {
            'registered_subject': self.registered_subject.pk,
            'report_datetime': timezone.now(),
            'maternal_visit': self.maternal_visit.id,
            'death_date': timezone.now().date(),
            'diagnosis_code': DiagnosisCode.objects.all().first().pk,
            'cause': Cause.objects.exclude(name__icontains='other').first().pk,
            'cause_category': CauseCategory.objects.exclude(name__icontains='other').first().pk,
            'medical_responsibility': MedicalResponsibility.objects.exclude(name__icontains='other').first().pk,
            'perform_autopsy': NO,
            'participant_hospitalized': YES,
            'reason_hospitalized': ReasonHospitalized.objects.exclude(name__icontains='other').first().pk,
            'death_cause': 'car accident',
            'days_hospitalized': 3,
            'illness_duration': 1,
        }

    def test_form_valid(self):
        form = MaternalDeathReportForm(data=self.data)
        # print(form.non_field_errors())
        self.assertTrue(form.is_valid())

    def test_maternal_validate_date_of_death(self):
        self.data['death_date'] = self.registered_subject.registration_datetime - relativedelta(weeks=2)
        form = MaternalDeathReportForm(data=self.data)
        self.assertIn(
            'Death date cannot be before date registered', form.errors.get('__all__') or [])

    def test_death_reason_hospitalized_yes(self):
        self.data['participant_hospitalized'] = YES
        self.data['reason_hospitalized'] = None
        self.data['days_hospitalized'] = 3
        form = MaternalDeathReportForm(data=self.data)
        self.assertIn(
            'If the participant was hospitalized, indicate the primary reason.',
            form.errors.get('__all__') or [])

    def test_death_reason_hospitalized_yes1(self):
        self.data['participant_hospitalized'] = NO
        self.data['reason_hospitalized'] = ReasonHospitalized.objects.exclude(name__icontains='other').first().pk
        self.data['days_hospitalized'] = None
        form = MaternalDeathReportForm(data=self.data)
        self.assertIn(
            'If the participant was not hospitalized, do not indicate the primary reason.',
            form.errors.get('__all__') or [])
