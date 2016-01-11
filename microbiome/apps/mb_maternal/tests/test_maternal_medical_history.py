from django.utils import timezone

from edc_appointment.models import Appointment
from edc_code_lists.models import WcsDxAdult
from edc_constants.constants import YES, NO, NOT_APPLICABLE, POS

from microbiome.apps.mb_list.models import ChronicConditions
from microbiome.apps.mb_maternal.forms import MaternalMedicalHistoryForm

from .base_maternal_test_case import BaseMaternalTestCase
from .factories import (
    MaternalEligibilityFactory, MaternalConsentFactory,
    MaternalVisitFactory, PostnatalEnrollmentFactory, AntenatalEnrollmentFactory)


class TestMaternalMedicalHistoryForm(BaseMaternalTestCase):

    def setUp(self):
        super(TestMaternalMedicalHistoryForm, self).setUp()

        maternal_eligibility = MaternalEligibilityFactory()
        maternal_consent = MaternalConsentFactory(
            registered_subject=maternal_eligibility.registered_subject)
        registered_subject = maternal_consent.registered_subject
        AntenatalEnrollmentFactory(
            registered_subject=registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            will_breastfeed=YES)
        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            will_breastfeed=YES)
        self.assertTrue(postnatal_enrollment.is_eligible)

        appointment_visit_1000 = Appointment.objects.get(
            registered_subject=registered_subject,
            visit_definition__code='1000M')
        appointment_visit_2000 = Appointment.objects.get(
            registered_subject=registered_subject,
            visit_definition__code='2000M')

        MaternalVisitFactory(appointment=appointment_visit_1000)
        maternal_visit_2000 = MaternalVisitFactory(appointment=appointment_visit_2000)

        chronicition = ChronicConditions.objects.exclude(
            name__icontains='other').exclude(name__icontains=NOT_APPLICABLE).first()
        who = WcsDxAdult.objects.get(short_name__icontains=NOT_APPLICABLE)
        self.data = {
            'report_datetime': timezone.now(),
            'maternal_visit': maternal_visit_2000.id,
            'chronic_since': NO,
            'chronic': [chronicition.id],
            'who_diagnosis': NO,
            'who': [who.id],
        }
        self.error_message_template = (
            'Participant reported no chronic disease at {enrollment}, '
            'yet you are reporting the participant has {condition}.')

    def test_chronicition_but_not_listed(self):
        """If indicated has chronic condition and no conditions supplied."""
        self.data['chronic_since'] = YES
        self.data['chronic'] = None
        maternal_medicalHistory_form = MaternalMedicalHistoryForm(data=self.data)
        errors = ''.join(maternal_medicalHistory_form.errors.get('__all__') or [])
        self.assertIn('You mentioned there are chronic conditions. Please list them.', errors)

    def test_no_chronicition_but_listed(self):
        """If indicated has NO chronic condition and conditions supplied"""
        maternal_medicalHistory_form = MaternalMedicalHistoryForm(data=self.data)
        errors = ''.join(maternal_medicalHistory_form.errors.get('__all__') or [])
        self.assertIn('You stated there are NO chronic conditions. Please correct', errors)

    def test_has_who_diagnosis_but_not_listed(self):
        """Test has no chronic condition, but has WHO diagnosis and no listing."""
        self.data['chronic_since'] = NO
        chronicition = ChronicConditions.objects.get(name__icontains=NOT_APPLICABLE)
        self.data['chronic'] = [chronicition.id]
        self.data['who_diagnosis'] = YES
        self.data['who'] = None
        maternal_medicalHistory_form = MaternalMedicalHistoryForm(data=self.data)
        errors = ''.join(maternal_medicalHistory_form.errors.get('__all__') or [])
        self.assertIn('You mentioned participant has WHO diagnosis. Please list them.', errors)

    def test_no_who_diagnosis_but_listed(self):
        """Test has no WHO diagnosis but they are listed."""
        chronicition = ChronicConditions.objects.get(name__icontains=NOT_APPLICABLE)
        self.data['chronic'] = [chronicition.id]
        who = WcsDxAdult.objects.get(short_name__icontains='Pneumocystis pneumonia')
        self.data['who'] = [who.id]
        form = MaternalMedicalHistoryForm(data=self.data)
        self.assertIn('You stated there are NO WHO diagnosess. Please correct',
                      form.errors.get('__all__'))
