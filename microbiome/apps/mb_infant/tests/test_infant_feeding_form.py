from django.utils import timezone
from datetime import date

from edc_registration.models import RegisteredSubject
from edc_appointment.models import Appointment
from edc_constants.constants import YES, NO, NEG, NOT_APPLICABLE

from microbiome.apps.mb.constants import INFANT
from microbiome.apps.mb_infant.forms import InfantFeedingForm
from microbiome.apps.mb_infant.models import InfantFeeding, InfantVisit
from microbiome.apps.mb_infant.tests.factories import InfantBirthFactory, InfantVisitFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory, MaternalLabourDelFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory, MaternalVisitFactory
from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory
from microbiome.apps.mb_infant.tests.factories import InfantFeedingFactory

from .base_test_case import BaseTestCase


class BaseTestInfantFeedingModel(InfantFeeding):
    class Meta:
        app_label = 'mb_infant'


class BaseTestInfantFeedingForm(InfantFeedingForm):

    class Meta:
        model = BaseTestInfantFeedingModel
        fields = '__all__'


class TestInfantFeedingForm(BaseTestCase):

    def setUp(self):
        super(TestInfantFeedingForm, self).setUp()

        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_eligibility.registered_subject

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject, visit_definition__code='2000M')
        maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        maternal_labour_del = MaternalLabourDelFactory(maternal_visit=maternal_visit)
        infant_registered_subject = RegisteredSubject.objects.get(
            subject_type=INFANT, relative_identifier=self.registered_subject.subject_identifier)
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
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2030')
        self.infant_visit_2030 = InfantVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=infant_registered_subject,
            visit_definition__code='2060')
        self.infant_visit = InfantVisitFactory(appointment=self.appointment)

        self.maternal_eligibility2 = MaternalEligibilityFactory()
        self.maternal_consent2 = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility2.registered_subject)
        self.registered_subject2 = self.maternal_eligibility2.registered_subject

        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject2,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        self.appointment2 = Appointment.objects.get(
            registered_subject=self.registered_subject2,
            visit_definition__code='1000M')
        self.maternal_visit2 = MaternalVisitFactory(appointment=self.appointment2)
        self.appointment2 = Appointment.objects.get(
            registered_subject=self.registered_subject2, visit_definition__code='2000M')
        maternal_visit2 = MaternalVisitFactory(appointment=self.appointment2)
        maternal_labour_del2 = MaternalLabourDelFactory(maternal_visit=maternal_visit2)
        infant_registered_subject2 = RegisteredSubject.objects.get(
            subject_type=INFANT, relative_identifier=self.registered_subject2.subject_identifier)
        self.infant_birth2 = InfantBirthFactory(
            registered_subject=infant_registered_subject2,
            maternal_labour_del=maternal_labour_del2)
        self.appointment2 = Appointment.objects.get(
            registered_subject=infant_registered_subject2,
            visit_definition__code='2000')
        self.infant_visit2 = InfantVisitFactory(appointment=self.appointment2)
        self.appointment2 = Appointment.objects.get(
            registered_subject=infant_registered_subject2,
            visit_definition__code='2010')
        self.infant_visit2 = InfantVisitFactory(appointment=self.appointment2)
        self.appointment2 = Appointment.objects.get(
            registered_subject=infant_registered_subject2,
            visit_definition__code='2030')
        self.infant_visit2 = InfantVisitFactory(appointment=self.appointment2)
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
        self.data['formula_intro_occur'] = NO
        feeding = BaseTestInfantFeedingForm(data=self.data)
        self.assertIn(u'If received formula milk | foods | liquids since last attended visit. '
                      'Please provide intro date', feeding.errors.get('__all__'))

    def test_validate_not_required_date(self):
        self.data['formula_intro_occur'] = YES
        self.data['other_feeding'] = NO
        self.data['formula_intro_date'] = date(2015, 11, 1)
        feeding = BaseTestInfantFeedingForm(data=self.data)
        self.assertIn(u'You mentioned no formula milk | foods | liquids received since last visit'
                      '. DO NOT PROVIDE DATE', feeding.errors.get('__all__'))

    def test_validate_no_first_reporting(self):
        self.data['formula_intro_occur'] = NO
        self.data['formula_intro_date'] = date(2015, 11, 1)
        self.data['is_first_formula'] = YES
        feeding = BaseTestInfantFeedingForm(data=self.data)
        self.assertIn(u'You mentioned that infant did not take formula, PLEASE DO NOT PROVIDE'
                      ' FIRST FORMULA USE INFO', feeding.errors.get('__all__'))

    def test_validate_date_first_formula(self):
        self.data['infant_visit'] = self.infant_visit_2030.id
        self.data['formula_intro_occur'] = YES
        self.data['formula_intro_date'] = date(2015, 11, 1)
        self.data['took_formula'] = YES
        self.data['is_first_formula'] = YES
        feeding = BaseTestInfantFeedingForm(data=self.data)
        self.assertIn(u'If this is a first reporting of infant formula please provide date'
                      ' and if date is estimated', feeding.errors.get('__all__'))

    def test_validate_no_date_first_formula(self):
        self.data['formula_intro_occur'] = NO
        self.data['formula_intro_date'] = date(2015, 11, 1)
        self.data['took_formula'] = YES
        self.data['date_first_formula'] = date(2015, 11, 1)
        self.data['est_date_first_formula'] = 'D'
        feeding = BaseTestInfantFeedingForm(data=self.data)
        self.assertIn(u'You mentioned that is not the first reporting of infant formula '
                      'PLEASE DO NOT PROVIDE DATE AND EST DATE', feeding.errors.get('__all__'))

    def test_validate_took_cows_milk(self):
        self.data['formula_intro_occur'] = NO
        self.data['formula_intro_date'] = date(2015, 11, 1)
        self.data['took_formula'] = NOT_APPLICABLE
        self.data['is_first_formula'] = NOT_APPLICABLE
        feeding = BaseTestInfantFeedingForm(data=self.data)
        self.assertIn(u'If infant took cows milk. Answer CANNOT be Not Applicable', feeding.errors.get('__all__'))

    def test_validate_no_cows_milk(self):
        self.data['formula_intro_occur'] = NO
        self.data['formula_intro_date'] = date(2015, 11, 1)
        self.data['took_formula'] = NOT_APPLICABLE
        self.data['is_first_formula'] = NOT_APPLICABLE
        self.data['cow_milk'] = NO
        self.data['cow_milk_yes'] = 'boiled'
        feeding = BaseTestInfantFeedingForm(data=self.data)
        self.assertIn(u'Infant did not take cows milk. Answer is NOT APPLICABLE', feeding.errors.get('__all__'))

    def test_save_infant_feeding(self):
        appointment = Appointment.objects.get(
            registered_subject=self.infant_birth.registered_subject.id,
            visit_definition__code='2010')
        visit_2010 = InfantVisit.objects.get(appointment=appointment)
        InfantFeedingFactory(infant_visit=visit_2010)
        options = {'infant_visit': self.infant_visit}
        self.assertEqual(InfantFeeding.objects.all().count(), 1)
        feeding = InfantFeedingFactory(**options)
        self.assertTrue(InfantFeeding.objects.all().count(), 2)
        self.assertTrue(feeding.last_att_sche_visit)

    def test_previous_infant_feeding_formula_intro_date_exists(self):
        appointment = Appointment.objects.get(
            registered_subject=self.infant_birth.registered_subject.id,
            visit_definition__code='2030')
        visit_2030 = InfantVisit.objects.get(appointment=appointment)
        InfantFeedingFactory(
            infant_visit=visit_2030, other_feeding=YES,
            formula_intro_occur=YES,
            formula_intro_date=timezone.now())
        self.data['other_feeding'] = YES
        self.data['formula_intro_occur'] = NO
        self.data['formula_intro_date'] = timezone.now()
        feeding = BaseTestInfantFeedingForm(data=self.data)
        self.assertIn(
            u'Infant has a previous date of formula milk | foods | liquids of {}, '
            'no need to give this date again.'.format(timezone.now().date()), feeding.errors.get('__all__'))

    def test_validate_formula_intro_yes_no_previous_intro_date(self):
        self.data['formula_intro_occur'] = YES
        feeding = BaseTestInfantFeedingForm(data=self.data)
        self.assertIn(
            u'There is no previous feeding with a formula introduction '
            'date, formula introduction should be NO and provide a '
            'formula introduction date.', feeding.errors.get('__all__'))
