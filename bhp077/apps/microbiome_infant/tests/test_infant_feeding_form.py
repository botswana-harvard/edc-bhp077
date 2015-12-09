from django.test import TestCase
from django import forms
from django.utils import timezone
from datetime import date

from edc.subject.registration.models import RegisteredSubject
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc_constants.constants import NEW, YES, NO, POS, NEG, NOT_REQUIRED

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome.constants import LIVE
from bhp077.apps.microbiome_infant.forms import InfantFeedingForm
from bhp077.apps.microbiome_infant.models import InfantFeeding
from bhp077.apps.microbiome_infant.tests.factories import InfantBirthFactory, InfantVisitFactory
from bhp077.apps.microbiome_infant.visit_schedule import InfantBirthVisitSchedule
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile, InfantProfile
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from bhp077.apps.microbiome_maternal.tests.factories import MaternalEligibilityFactory, MaternalVisitFactory
from bhp077.apps.microbiome_maternal.tests.factories import PostnatalEnrollmentFactory
from bhp077.apps.microbiome_maternal.visit_schedule import PostnatalEnrollmentVisitSchedule


class BaseTestInfantFeedingModel(InfantFeeding):
    class Meta:
        app_label = 'microbiome_infant'


class BaseTestInfantFeedingForm(InfantFeedingForm):

    class Meta:
        model = BaseTestInfantFeedingModel
        fields = '__all__'


class TestInfantFeedingForm(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
            site_lab_profiles.register(InfantProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()
        InfantBirthVisitSchedule().build()

        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_eligibility.registered_subject

        postnatal = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES)
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M')
        maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)
        infant_registered_subject = RegisteredSubject.objects.get(
            subject_type='infant', relative_identifier=self.registered_subject.subject_identifier)
        self.infant_birth = InfantBirthFactory(
            registered_subject=infant_registered_subject,
            maternal_labour_del=maternal_labour_del)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2000')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2010')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.data = {
            'report_datetime': timezone.now(),
            'infant_birth': self.infant_birth.id,
            'infant_visit': self.infant_visit.id,
            'last_att_sche_visit': date(2015, 9, 15),
            'other_feeding': YES,
            'formula_intro_occur': YES,
            'formula_intro_date': None,
            'took_formula': NO,
            'is_first_formula': NO,
            'date_first_formula': None,
            'est_date_first_formula': None,
            'water': YES,
            'juice': YES,
            'cow_milk': YES,
            'cow_milk_yes': 'N/A',
            'other_milk': YES,
            'other_milk_animal': YES,
            'milk_boiled': YES,
            'fruits_veg': YES,
            'cereal_porridge': YES,
            'solid_liquid': YES,
            'rehydration_salts': YES,
            'water_used': 'N/A',
            'water_used_other': None,
            'ever_breastfeed': YES,
            'complete_weaning': YES,
            'weaned_completely': YES,
            'most_recent_bm': None,
            'times_breastfed': '<1 per week'
        }

    def test_validate_formula_date_intro(self):
        self.data['infant_birth'] = self.infant_visit.id
        self.data['infant_birth'] = self.infant_visit.id
        feeding = BaseTestInfantFeedingForm(data=self.data)
        self.assertIn(u'If received formula milk | foods | liquids since last attended visit. '
                      'Please provide intro date', feeding.errors.get('__all__'))

    def test_validate_not_required_date(self):
        self.data['infant_birth'] = self.infant_visit.id
        self.data['infant_birth'] = self.infant_visit.id
        self.data['other_feeding'] = NO
        self.data['formula_intro_date'] = date(2015, 11, 1)
        feeding = BaseTestInfantFeedingForm(data=self.data)
        self.assertIn(u'You mentioned no formula milk | foods | liquids received since last visit'
                      '. DO NOT PROVIDE DATE', feeding.errors.get('__all__'))

    def test_validate_no_first_reporting(self):
        self.data['infant_birth'] = self.infant_visit.id
        self.data['infant_birth'] = self.infant_visit.id
        self.data['formula_intro_date'] = date(2015, 11, 1)
        self.data['is_first_formula'] = YES
        feeding = BaseTestInfantFeedingForm(data=self.data)
        self.assertIn(u'You mentioned that infant did not take formula, PLEASE DO NOT PROVIDE'
                      ' FIRST FORMULA USE INFO', feeding.errors.get('__all__'))

    def test_validate_date_first_formula(self):
        self.data['infant_birth'] = self.infant_visit.id
        self.data['infant_birth'] = self.infant_visit.id
        self.data['formula_intro_date'] = date(2015, 11, 1)
        self.data['took_formula'] = YES
        self.data['is_first_formula'] = YES
        feeding = BaseTestInfantFeedingForm(data=self.data)
        self.assertIn(u'If this is a first reporting of infant formula please provide date'
                      ' and if date is estimated', feeding.errors.get('__all__'))

    def test_validate_no_date_first_formula(self):
        self.data['infant_birth'] = self.infant_visit.id
        self.data['infant_birth'] = self.infant_visit.id
        self.data['formula_intro_date'] = date(2015, 11, 1)
        self.data['took_formula'] = YES
        self.data['date_first_formula'] = date(2015, 11, 1)
        self.data['est_date_first_formula'] = 'D'
        feeding = BaseTestInfantFeedingForm(data=self.data)
        self.assertIn(u'You mentioned that is not the first reporting of infant formula '
                      'PLEASE DO NOT PROVIDE DATE AND EST DATE', feeding.errors.get('__all__'))

    def test_validate_took_cows_milk(self):
        self.data['infant_birth'] = self.infant_visit.id
        self.data['infant_birth'] = self.infant_visit.id
        self.data['took_formula'] = YES
        self.data['formula_intro_date'] = date(2015, 11, 1)
        feeding = BaseTestInfantFeedingForm(data=self.data)
        self.assertIn(u'If infant took cows milk. Answer CANNOT be Not Applicable', feeding.errors.get('__all__'))

    def test_validate_no_cows_milk(self):
        self.data['infant_birth'] = self.infant_visit.id
        self.data['infant_birth'] = self.infant_visit.id
        self.data['took_formula'] = YES
        self.data['formula_intro_date'] = date(2015, 11, 1)
        self.data['cow_milk'] = NO
        self.data['cow_milk_yes'] = 'boiled'
        feeding = BaseTestInfantFeedingForm(data=self.data)
        self.assertIn(u'Infant did not take cows milk. Answer is NOT APPLICABLE', feeding.errors.get('__all__'))
