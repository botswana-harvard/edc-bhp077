from django.test import TestCase
from django.utils import timezone

from bhp077.apps.microbiome_infant.models import InfantVisit
from bhp077.apps.microbiome_infant.forms import InfantFeedingForm

from edc.subject.registration.models import RegisteredSubject
from edc.entry_meta_data.models import ScheduledEntryMetaData, RequisitionMetaData
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc_constants.constants import NEW, POS, YES, NO, NOT_APPLICABLE

from bhp077.apps.microbiome.constants import LIVE
from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_maternal.tests.factories import (MaternalEligibilityFactory, AntenatalEnrollmentFactory,
    MaternalVisitFactory)
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from bhp077.apps.microbiome_maternal.tests.factories import PostnatalEnrollmentFactory, SexualReproductiveHealthFactory
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile, InfantProfile
from bhp077.apps.microbiome_maternal.models import PostnatalEnrollment

from bhp077.apps.microbiome_maternal.visit_schedule import AntenatalEnrollmentVisitSchedule, PostnatalEnrollmentVisitSchedule
from bhp077.apps.microbiome_infant.visit_schedule import InfantBirthVisitSchedule
from bhp077.apps.microbiome_infant.tests.factories import \
    (InfantBirthFactory, InfantBirthDataFactory, InfantVisitFactory, InfantBirthFeedVaccineFactory)
from bhp077.apps.microbiome_infant.models import InfantBirth


class TestInfantFeedingForm(TestCase):

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

        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject

        post = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            verbal_hiv_status=POS,
            evidence_hiv_status=YES,
        )
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M'
        )
        maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)

        registered_subject_infant = RegisteredSubject.objects.get(
            subject_type='infant', relative_identifier=self.registered_subject.subject_identifier
        )
        self.infant_birth = InfantBirthFactory(
            registered_subject=registered_subject_infant,
            maternal_labour_del=maternal_labour_del,
        )
        self.appointment = Appointment.objects.get(
            registered_subject=registered_subject_infant,
            visit_definition__code='2000'
        )
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)
        self.data = {
            'report_datetime': timezone.now(),
            'infant_birth':self.infant_birth.id,
            'infant_visit': self.infant_visit.id,
            'last_att_sche_visit': timezone.now().date(),
            'other_feeding': YES,
            'formula_intro_occur': YES,
            'formula_date': timezone.now().date(),
            'formula': YES,
            'water': YES,
            'juice': YES,
            'cow_milk': YES,
            'cow_milk_yes': NOT_APPLICABLE, # 'unboiled',
            'other_milk': YES,
            'other_milk_animal': 'NA',
            'milk_boiled': NO,
            'fruits_veg':  YES,
            'cereal_porridge': YES,
            'solid_liquid': YES,
            'rehydration_salts': YES,
            'water_used': 'Water boiled immediately before use',
            'water_used_other': '',
            'reason_rcv_formula': 'no milk',
            'reason_rcv_fm_other': '',
            'ever_breastfeed': YES,
            'complete_weaning': YES,
            'times_breastfed': '<1 per week',
            'most_recent_bm': timezone.now().date(),
            'weaned_completely': YES,
            'vLargeTextField': ''
        }

    def test_validate_formula_intro_occur_valid(self):
        "If formula_intro_occur eq to YES then formula_date is required. "
        self.data['infant_birth'] = self.infant_visit.id
        infant_feeding_form = InfantFeedingForm(data=self.data)
        #print infant_feeding_form.errors
        self.assertTrue(infant_feeding_form.is_valid())

    def test_validate_formula_intro_occur_not_valid(self):
        "If formula_intro_occur eq to YES then You should answer (yes) either on Q9, Q10, Q11, Q12, Q15, Q16 or Q17."
        for question in [
            'juice', 'cow_milk', 'boiled', 'other_milk', 'fruits_veg', 'cereal_porridge', 'solid_liquid']:
            self.data[question] = NO
        infant_feeding_form = InfantFeedingForm(data=self.data)
        self.assertIn(u'You should answer (yes) either on Q9, Q10, Q11, Q12, Q15, Q16 or Q17.',
                      infant_feeding_form.errors.get('__all__'))

    def test_validate_formula_intro_occur_valid2(self):
        "If formula_intro_occur eq to YES then You should answer (yes) either on Q9, Q10, Q11, Q12, Q15, Q16 or Q17."
        for question in [
            'juice', 'cow_milk', 'boiled', 'other_milk', 'fruits_veg', 'cereal_porridge', 'solid_liquid']:
            self.data[question] = NO
        del self.data['other_milk_animal']
        self.data['juice'] = YES
        self.data['cow_milk_yes'] = 'boiled'
        infant_feeding_form = InfantFeedingForm(data=self.data)
        print infant_feeding_form.errors
        self.assertTrue(infant_feeding_form.is_valid())

    def test_validate_cow_milk_not_valid1(self):
        for question in [
            'juice', 'cow_milk', 'boiled', 'other_milk', 'fruits_veg', 'cereal_porridge', 'solid_liquid']:
            self.data[question] = NO
        self.data['juice'] = YES
        self.data['cow_milk'] = YES
        self.data['cow_milk_yes'] = 'cow_milk_yes'
        infant_feeding_form = InfantFeedingForm(data=self.data)
        self.assertIn(u'Please, provide answer for Q11.',
                      infant_feeding_form.errors.get('__all__'))

    def test_validate_cow_milk_not_valid2(self):
        for question in [
            'juice', 'cow_milk', 'boiled', 'other_milk', 'fruits_veg', 'cereal_porridge', 'solid_liquid']:
            self.data[question] = NO
        self.data['juice'] = YES
        self.data['cow_milk'] = NO
        self.data['cow_milk_yes'] = NOT_APPLICABLE
        infant_feeding_form = InfantFeedingForm(data=self.data)
        self.assertIn(u'The answer to question 11 cannot be NOT APPLICABLE.',
                      infant_feeding_form.errors.get('__all__'))

    def test_validate_other_milk_not_valid(self):
        for question in [
            'juice', 'cow_milk', 'boiled', 'other_milk', 'fruits_veg', 'cereal_porridge', 'solid_liquid']:
            self.data[question] = NO
        self.data['other_milk'] = YES
        self.data['cow_milk_yes'] = 'boiled'
        self.data['other_milk_animal'] = ''
        infant_feeding_form = InfantFeedingForm(data=self.data)
        self.assertIn(u'Please, provide answer for question 13.', infant_feeding_form.errors.get('__all__'))

    def test_validate_other_milk_not_valid1(self):
        for question in [
            'juice', 'cow_milk', 'boiled', 'other_milk', 'fruits_veg', 'cereal_porridge', 'solid_liquid']:
            self.data[question] = NO
        self.data['other_milk'] = YES
        self.data['cow_milk_yes'] = 'boiled'
        self.data['milk_boiled'] = NOT_APPLICABLE
        infant_feeding_form = InfantFeedingForm(data=self.data)
        self.assertIn(u'Do not select NOT APPLICABLE for question 14, if the answer to Q12 is yes.',
                      infant_feeding_form.errors.get('__all__'))

    def test_validate_other_milk_animal_valid(self):
        for question in [
            'juice', 'cow_milk', 'boiled', 'other_milk', 'fruits_veg', 'cereal_porridge', 'solid_liquid']:
            self.data[question] = NO
        self.data['other_milk'] = NO
        self.data['juice'] = YES
        self.data['cow_milk_yes'] = 'boiled'
        self.data['other_milk_animal'] = 'donkey'
        infant_feeding_form = InfantFeedingForm(data=self.data)
        self.assertIn(u'Do not provide answer for question 13.',
                      infant_feeding_form.errors.get('__all__'))

    def test_validate_ever_breastfeed(self):
        for question in [
            'juice', 'cow_milk', 'boiled', 'other_milk', 'fruits_veg', 'cereal_porridge', 'solid_liquid']:
            self.data[question] = NO
        self.data['juice'] = YES
        del self.data['other_milk_animal']
        self.data['ever_breastfeed'] = NO
        self.data['cow_milk_yes'] = 'boiled'
        self.data['complete_weaning'] = YES
        infant_feeding_form = InfantFeedingForm(data=self.data)
        self.assertIn(u'Please, select NOT APPLICABLE for question 24.',
                      infant_feeding_form.errors.get('__all__'))

    def test_validate_ever_breastfeed1(self):
        for question in [
            'juice', 'cow_milk', 'boiled', 'other_milk', 'fruits_veg', 'cereal_porridge', 'solid_liquid']:
            self.data[question] = NO
        del self.data['other_milk_animal']
        self.data['juice'] = YES
        self.data['cow_milk_yes'] = 'boiled'
        self.data['ever_breastfeed'] = YES
        self.data['complete_weaning'] = NOT_APPLICABLE
        infant_feeding_form = InfantFeedingForm(data=self.data)
        self.assertIn(u'Please, do not select NOT APPLICABLE for question 24, select appropriate answer.',
                      infant_feeding_form.errors.get('__all__'))

    def test_validate_ever_breastfeed_valid(self):
        for question in [
            'juice', 'cow_milk', 'boiled', 'other_milk', 'fruits_veg', 'cereal_porridge', 'solid_liquid']:
            self.data[question] = NO
        del self.data['other_milk_animal']
        self.data['juice'] = YES
        self.data['cow_milk_yes'] = 'boiled'
        self.data['ever_breastfeed'] = NO
        self.data['complete_weaning'] = NOT_APPLICABLE
        infant_feeding_form = InfantFeedingForm(data=self.data)
        self.assertTrue(infant_feeding_form.is_valid())

    def test_validate_ever_breastfeed_valid1(self):
        for question in [
            'juice', 'cow_milk', 'boiled', 'other_milk', 'fruits_veg', 'cereal_porridge', 'solid_liquid']:
            self.data[question] = NO
        del self.data['other_milk_animal']
        self.data['juice'] = YES
        self.data['cow_milk_yes'] = 'boiled'
        self.data['ever_breastfeed'] = YES
        self.data['complete_weaning'] = NO
        infant_feeding_form = InfantFeedingForm(data=self.data)
        self.assertTrue(infant_feeding_form.is_valid())
