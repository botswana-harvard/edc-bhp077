from dateutil.relativedelta import relativedelta

from django.utils import timezone

from edc_appointment.models import Appointment
from edc_constants.constants import YES, NO, NEG, SCHEDULED
from edc_death_report.models import Cause, CauseCategory, MedicalResponsibility, DiagnosisCode, ReasonHospitalized
from edc_registration.models import RegisteredSubject

from microbiome.apps.mb_maternal.forms import MaternalDeathReportForm

from .base_maternal_test_case import BaseMaternalTestCase
from .factories import (
    PostnatalEnrollmentFactory, MaternalConsentFactory,
    MaternalLabourDelFactory, MaternalEligibilityFactory, MaternalVisitFactory)


class TestMaternalDeathReportForm(BaseMaternalTestCase):

    def setUp(self):
        super(TestMaternalDeathReportForm, self).setUp()
        maternal_eligibility = MaternalEligibilityFactory()
        registered_subject = RegisteredSubject.objects.get(
            pk=maternal_eligibility.registered_subject.pk)
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=registered_subject)
        self.registered_subject = RegisteredSubject.objects.get(pk=registered_subject.pk)

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        self.assertTrue(postnatal_enrollment.is_eligible)
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        MaternalVisitFactory(appointment=appointment, reason=SCHEDULED)
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='2000M')
        self.maternal_visit = MaternalVisitFactory(
            appointment=self.appointment, reason=SCHEDULED)
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
