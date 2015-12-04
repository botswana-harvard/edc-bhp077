from django.test import TestCase
from django.utils import timezone
from datetime import date

from edc.subject.registration.models import RegisteredSubject
from edc.entry_meta_data.models import ScheduledEntryMetaData
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from edc.subject.code_lists.models import WcsDxAdult

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_maternal.tests.factories import (MaternalEligibilityFactory, AntenatalEnrollmentFactory,
    MaternalVisitFactory)
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory
from bhp077.apps.microbiome_list.models import ChronicConditions
from bhp077.apps.microbiome_maternal.tests.factories import PostnatalEnrollmentFactory
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from bhp077.apps.microbiome_maternal.forms import MaternalMedicalHistoryForm

from ..visit_schedule import AntenatalEnrollmentVisitSchedule, PostnatalEnrollmentVisitSchedule


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

        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject
        self.postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            will_breastfeed=YES
        )
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='2000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        c = ChronicConditions.objects.create(name=NOT_APPLICABLE, short_name=NOT_APPLICABLE, field_name='chronic_cond')
        who = WcsDxAdult.objects.create(code=NOT_APPLICABLE, short_name=NOT_APPLICABLE, long_name=NOT_APPLICABLE)
        self.data = {
            'report_datetime': timezone.now(),
            'maternal_visit': self.maternal_visit.id,
            'chronic_cond_since': NO,
            'chronic_cond': [c.id],
            'who_diagnosis': NO,
            'wcs_dx_adult': [who.id],
        }

    def test_valid(self):
        maternal_medicalHistory_form = MaternalMedicalHistoryForm(data=self.data)
        self.assertTrue(maternal_medicalHistory_form.is_valid())

    def test_chronic_cond_1(self):
        """If indicated has chronic condition and no conditions supplied."""
        self.data['chronic_cond_since'] = YES
        maternal_medicalHistory_form = MaternalMedicalHistoryForm(data=self.data)
        errors = ''.join(maternal_medicalHistory_form.errors.get('__all__'))
        self.assertIn('You stated there ARE chronic condition', errors)

    def test_chronic_cond_2(self):
        """If indicated has NO chronic condition and conditions supplied"""
        chronic = ChronicConditions.objects.create(name='Diabetes', short_name='Diabetes', field_name='chronic_cond')
        self.data['chronic_cond'] = [chronic.id]
        maternal_medicalHistory_form = MaternalMedicalHistoryForm(data=self.data)
        errors = ''.join(maternal_medicalHistory_form.errors.get('__all__'))
        self.assertIn('You stated there are NO chronic conditions.', errors)

    def test_who_diagnosis_1(self):
        self.data['who_diagnosis'] = YES
        maternal_medicalHistory_form = MaternalMedicalHistoryForm(data=self.data)
        errors = ''.join(maternal_medicalHistory_form.errors.get('__all__'))
        self.assertIn('You stated there ARE WHO diagnoses', errors)

    def test_who_diagnosis_2(self):
        who_dx = WcsDxAdult.objects.create(code='Meningitis', short_name='Meningitis', long_name='Meningitis')
        self.data['wcs_dx_adult'] = [who_dx.id]
        maternal_medicalHistory_form = MaternalMedicalHistoryForm(data=self.data)
        errors = ''.join(maternal_medicalHistory_form.errors.get('__all__'))
        self.assertIn('You stated there are NO WHO diagnoses', errors)
