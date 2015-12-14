from django.test import TestCase
from django.utils import timezone

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc_constants.constants import YES, NO, NOT_APPLICABLE, POS
from edc.subject.code_lists.models import WcsDxAdult

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_maternal.tests.factories import (MaternalEligibilityFactory)
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory
from bhp077.apps.microbiome_maternal.tests.factories import PostnatalEnrollmentFactory, AntenatalEnrollmentFactory
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from bhp077.apps.microbiome_maternal.forms import MaternalMedicalHistoryForm

from bhp077.apps.microbiome_maternal.models.postnatal_enrollment import PostnatalEnrollment
from bhp077.apps.microbiome_maternal.models.antenatal_enrollment import AntenatalEnrollment
from bhp077.apps.microbiome_list.models.chronic_conditions import ChronicConditions

from ..visit_schedule import AntenatalEnrollmentVisitSchedule, PostnatalEnrollmentVisitSchedule

from .factories import MaternalVisitFactory


class TestMaternalMedicalHistoryForm(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        AntenatalEnrollmentVisitSchedule().build()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()

        self.maternal_eligibility_1 = MaternalEligibilityFactory()
        self.maternal_eligibility_2 = MaternalEligibilityFactory()

        self.maternal_consent_1 = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility_1.registered_subject)
        self.maternal_consent_2 = MaternalConsentFactory(
            study_site=self.maternal_consent_1.study_site,
            registered_subject=self.maternal_eligibility_2.registered_subject)

        self.registered_subject_1 = self.maternal_consent_1.registered_subject
        self.registered_subject_2 = self.maternal_consent_2.registered_subject

        self.antenatal_enrollment = AntenatalEnrollmentFactory(
            registered_subject=self.registered_subject_1,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            will_breastfeed=YES)
        self.postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject_2,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            will_breastfeed=YES)
        self.assertTrue(self.postnatal_enrollment.is_eligible)
        self.appointment_visit_2000 = Appointment.objects.get(
            registered_subject=self.registered_subject_2,
            visit_definition__code='2000M')
        self.appointment_visit_1000 = Appointment.objects.get(
            registered_subject=self.registered_subject_1,
            visit_definition__code='1000M')

        self.maternal_visit_1000 = MaternalVisitFactory(appointment=self.appointment_visit_1000)
        self.maternal_visit_2000 = MaternalVisitFactory(appointment=self.appointment_visit_2000)
        chronic_condition = ChronicConditions.objects.exclude(
            name__icontains='other').exclude(name__icontains=NOT_APPLICABLE).first()
        wcs_dx_adult = WcsDxAdult.objects.get(short_name__icontains=NOT_APPLICABLE)
        self.data = {
            'report_datetime': timezone.now(),
            'maternal_visit': self.maternal_visit_2000.id,
            'chronic_cond_since': NO,
            'chronic_cond': [chronic_condition.id],
            'who_diagnosis': NO,
            'wcs_dx_adult': [wcs_dx_adult.id],
        }
        self.error_message_template = (
            'Participant reported no chronic disease at {enrollment}, '
            'yet you are reporting the participant has {condition}.')

    def test_valid(self):
        maternal_medicalHistory_form = MaternalMedicalHistoryForm(data=self.data)
        self.assertTrue(maternal_medicalHistory_form.is_valid())

    def test_chronic_cond_1(self):
        """If indicated has chronic condition and no conditions supplied."""
        self.data['chronic_cond_since'] = YES
        chronic_condition = ChronicConditions.objects.exclude(
            name__icontains='other').exclude(name__icontains=NOT_APPLICABLE).first()
        self.data['chronic_cond'] = [chronic_condition.id]
        maternal_medicalHistory_form = MaternalMedicalHistoryForm(data=self.data)
        errors = ''.join(maternal_medicalHistory_form.errors.get('__all__') or [])
        self.assertIn('You stated there ARE chronic condition', errors)

    def test_chronic_cond_2(self):
        """If indicated has NO chronic condition and conditions supplied"""
        chronic_condition = ChronicConditions.objects.exclude(
            name__icontains='other').exclude(name__icontains=NOT_APPLICABLE).first()
        self.data['chronic_cond'] = [chronic_condition.id]
        maternal_medicalHistory_form = MaternalMedicalHistoryForm(data=self.data)
        errors = ''.join(maternal_medicalHistory_form.errors.get('__all__') or [])
        self.assertIn('You stated there are NO chronic conditions.', errors)

    def test_who_diagnosis_1(self):
        """Assert raises if has WHO diagnosis but they are not listed."""
        self.data['who_diagnosis'] = YES
        self.data['chronic_cond_since'] = YES
        chronic_condition = ChronicConditions.objects.exclude(
            name__icontains='other').exclude(name__icontains=NOT_APPLICABLE).first()
        self.data['chronic_cond'] = [chronic_condition.id]
        maternal_medicalHistory_form = MaternalMedicalHistoryForm(data=self.data)
        errors = ''.join(maternal_medicalHistory_form.errors.get('__all__') or [])
        self.assertIn('You stated there ARE WHO diagnoses', errors)

    def test_who_diagnosis_2(self):
        """Assert raises if does not have WHO diagnosis but they are not listed."""
        wcs_dx_adult = WcsDxAdult.objects.all().first()
        self.data['wcs_dx_adult'] = [wcs_dx_adult.id]
        maternal_medicalHistory_form = MaternalMedicalHistoryForm(data=self.data)
        errors = ''.join(maternal_medicalHistory_form.errors.get('__all__') or [])
        self.assertIn('You stated there are NO WHO diagnoses', errors)

    def test_chronic_conditions_vs_antenatal_enrollment(self):
        """Test any reported chronic conditions matches what was report at antenatal enrollment."""
        conditions = ['Tuberculosis', 'Chronic Diabetes', 'Chronic Hypertension']
        for condition in conditions:
            chronic_condition = ChronicConditions.objects.get(
                name=condition,
                short_name=condition,
                field_name='chronic_cond'
            )
            self.data['maternal_visit'] = self.maternal_visit_1000.id
            self.data['chronic_cond'] = [chronic_condition.id]
            self.data['chronic_cond_since'] = YES
            maternal_medicalHistory_form = MaternalMedicalHistoryForm(data=self.data)
            errors = ''.join(maternal_medicalHistory_form.errors.get('__all__') or [])
            error_msg = self.error_message_template.format(
                enrollment=AntenatalEnrollment._meta.verbose_name,
                condition=condition)
            self.assertIn(error_msg, errors)

    def test_chronic_conditions_vs_postnatal_enrollment(self):
        """Test any reported chronic conditions matches what was report at postnatal enrollment."""
        conditions = ['Tuberculosis', 'Chronic Diabetes', 'Chronic Hypertension']
        for condition in conditions:
            chronic_condition = ChronicConditions.objects.get(
                name=condition,
                short_name=condition,
                field_name='chronic_cond'
            )
            self.data['maternal_visit'] = self.maternal_visit_2000.id
            self.data['chronic_cond'] = [chronic_condition.id]
            self.data['chronic_cond_since'] = YES
            maternal_medicalHistory_form = MaternalMedicalHistoryForm(data=self.data)
            errors = ''.join(maternal_medicalHistory_form.errors.get('__all__') or [])
            error_msg = self.error_message_template.format(
                enrollment=PostnatalEnrollment._meta.verbose_name,
                condition=condition)
            self.assertIn(error_msg, errors)
