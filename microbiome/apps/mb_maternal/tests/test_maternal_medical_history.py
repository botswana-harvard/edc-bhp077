from django import forms
from django.test import TestCase
from django.utils import timezone

from edc.core.bhp_variables.tests.factories.study_site_factory import StudySiteFactory
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.code_lists.models import WcsDxAdult
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc_constants.constants import YES, NO, NOT_APPLICABLE, POS, NEG

from microbiome.apps.mb.app_configuration.classes import MicrobiomeConfiguration
from microbiome.apps.mb_maternal.tests.factories import (MaternalEligibilityFactory)
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory
from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory, AntenatalEnrollmentFactory
from microbiome.apps.mb_lab.lab_profiles import MaternalProfile
from microbiome.apps.mb_maternal.forms import MaternalMedicalHistoryForm

from microbiome.apps.mb_maternal.models.postnatal_enrollment import PostnatalEnrollment
from microbiome.apps.mb_maternal.models.antenatal_enrollment import AntenatalEnrollment
from microbiome.apps.mb_list.models.chronic_conditions import ChronicConditions

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
        self.appointment_visit_1000 = Appointment.objects.get(
            registered_subject=self.registered_subject_1,
            visit_definition__code='1000M')
        self.appointment_visit_2000 = Appointment.objects.get(
            registered_subject=self.registered_subject_2,
            visit_definition__code='2000M')

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

    def test_chronic_condition_but_not_listed(self):
        """If indicated has chronic condition and no conditions supplied."""
        self.data['chronic_cond_since'] = YES
        self.data['chronic_cond'] = None
        maternal_medicalHistory_form = MaternalMedicalHistoryForm(data=self.data)
        errors = ''.join(maternal_medicalHistory_form.errors.get('__all__') or [])
        self.assertIn('You mentioned there are chronic conditions. Please list them.', errors)

    def test_no_chronic_condition_but_listed(self):
        """If indicated has NO chronic condition and conditions supplied"""
        maternal_medicalHistory_form = MaternalMedicalHistoryForm(data=self.data)
        errors = ''.join(maternal_medicalHistory_form.errors.get('__all__') or [])
        self.assertIn('You stated there are NO chronic conditions. Please correct', errors)

    def test_has_who_diagnosis_but_not_listed(self):
        """Test has no chronic condition, but has WHO diagnosis and no listing."""
        self.data['chronic_cond_since'] = NO
        chronic_condition = ChronicConditions.objects.get(name__icontains=NOT_APPLICABLE)
        self.data['chronic_cond'] = [chronic_condition.id]
        self.data['who_diagnosis'] = YES
        self.data['wcs_dx_adult'] = None
        maternal_medicalHistory_form = MaternalMedicalHistoryForm(data=self.data)
        errors = ''.join(maternal_medicalHistory_form.errors.get('__all__') or [])
        self.assertIn('You mentioned participant has WHO diagnosis. Please list them.', errors)

    def test_no_who_diagnosis_but_listed(self):
        """Test has no WHO diagnosis but they are listed."""
        chronic_condition = ChronicConditions.objects.get(name__icontains=NOT_APPLICABLE)
        self.data['chronic_cond'] = [chronic_condition.id]
        wcs_dx_adult = WcsDxAdult.objects.get(short_name__icontains='Pneumocystis pneumonia')
        self.data['wcs_dx_adult'] = [wcs_dx_adult.id]
        form = MaternalMedicalHistoryForm(data=self.data)
        self.assertIn('You stated there are NO WHO diagnosess. Please correct',
                      form.errors.get('__all__'))
