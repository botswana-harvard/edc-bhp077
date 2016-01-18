from django.utils import timezone
from datetime import timedelta

from edc_appointment.models import Appointment
from edc_code_lists.models import WcsDxAdult
from edc_constants.constants import YES, NO, NOT_APPLICABLE, POS, NEG

from microbiome.apps.mb_list.models import ChronicConditions
from microbiome.apps.mb_maternal.forms import MaternalMedicalHistoryForm
from microbiome.apps.mb_maternal.models import MaternalVisit

from .base_test_case import BaseTestCase
from .factories import (
    MaternalEligibilityFactory, MaternalConsentFactory,
    MaternalVisitFactory, PostnatalEnrollmentFactory, AntenatalEnrollmentFactory)


class TestMaternalMedicalHistoryForm(BaseTestCase):

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

    def test_who_stage_diagnosis_for_neg_mother(self):
        """Test that NEG mother can only answer N/A for who_diagnosis"""
        eligibility = MaternalEligibilityFactory()
        consent = MaternalConsentFactory(
            registered_subject=eligibility.registered_subject,
            study_site='50')
        registered_subject = consent.registered_subject
        antenatal_enrollment = AntenatalEnrollmentFactory(
            gestation_wks=35,
            week32_test=YES,
            week32_result=NEG,
            week32_test_date=timezone.now().date() - timedelta(weeks=3),
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            valid_regimen=NOT_APPLICABLE,
            valid_regimen_duration=NOT_APPLICABLE,
            rapid_test_done=NOT_APPLICABLE,
            registered_subject=registered_subject)
        subject_appointment = Appointment.objects.get(
            registered_subject=antenatal_enrollment.registered_subject,
            visit_definition__code='1000M')
        maternal_visit = MaternalVisit.objects.get(appointment=subject_appointment)
        self.data['maternal_visit'] = maternal_visit.id
        self.data['chronic'] = None
        form = MaternalMedicalHistoryForm(data=self.data)
        self.assertIn(
            'Mother is NEG. WHO stage diagnosis should be Not applicable.',
            form.errors.get('__all__'))

    def test_who_stage_diagnosis_cannot_be_not_applicable_for_pos_mother(self):
        """Test that POS mother cannot answer N/A for who_diagnosis"""
        self.data['who_diagnosis'] = NOT_APPLICABLE
        self.data['chronic'] = None
        form = MaternalMedicalHistoryForm(data=self.data)
        self.assertIn(
            'Mother is POS. WHO stage diagnosis cannot be N/A.',
            form.errors.get('__all__'))

    def test_neg_mother_cannot_make_who_listing(self):
        """Test a NEG mother with a who listing"""
        eligibility = MaternalEligibilityFactory()
        consent = MaternalConsentFactory(
            registered_subject=eligibility.registered_subject,
            study_site='50')
        registered_subject = consent.registered_subject
        antenatal_enrollment = AntenatalEnrollmentFactory(
            gestation_wks=35,
            week32_test=YES,
            week32_result=NEG,
            week32_test_date=timezone.now().date() - timedelta(weeks=3),
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            valid_regimen=NOT_APPLICABLE,
            valid_regimen_duration=NOT_APPLICABLE,
            rapid_test_done=NOT_APPLICABLE,
            registered_subject=registered_subject)
        subject_appointment = Appointment.objects.get(
            registered_subject=antenatal_enrollment.registered_subject,
            visit_definition__code='1000M')
        maternal_visit = MaternalVisit.objects.get(appointment=subject_appointment)
        who_list = WcsDxAdult.objects.exclude(short_name__icontains=NOT_APPLICABLE).first()
        self.data['maternal_visit'] = maternal_visit.id
        self.data['chronic'] = NOT_APPLICABLE
        self.data['who_diagnosis'] = NOT_APPLICABLE
        self.data['who'] = [who_list.id]
        form = MaternalMedicalHistoryForm(data=self.data)
        self.assertIn(
            "Mother is NEG and cannot have a WHO diagnosis listing. "
            "Answer should be 'Not Applicable', Please Correct.",
            form.errors.get('__all__'))
