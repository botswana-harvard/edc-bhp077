from dateutil.relativedelta import relativedelta

from django.test import TestCase
from django.utils import timezone

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc_appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc_constants.choices import YES, NO, NOT_APPLICABLE, POS

from microbiome.apps.mb.app_configuration.classes import MicrobiomeConfiguration
from microbiome.apps.mb_lab.lab_profiles import MaternalProfile
from microbiome.apps.mb_maternal.forms import (MaternalLabourDelForm, MaternalLabDelClinicForm)

from ..visit_schedule import PostnatalEnrollmentVisitSchedule

from .base_maternal_test_case import BaseMaternalTestCase
from .factories import (PostnatalEnrollmentFactory, MaternalLabourDelFactory, MaternalVisitFactory,
                        MaternalEligibilityFactory, MaternalConsentFactory)


class TestMaternalLabourDel(BaseMaternalTestCase):
    """Test eligibility of a mother for labour and delivery."""

    def setUp(self):
        super(TestMaternalLabourDel, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject,
            study_site=self.study_site)
        self.registered_subject = self.maternal_consent.registered_subject
        self.postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            will_breastfeed=YES)
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='2000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.data = {
            'maternal_visit': self.maternal_visit.id,
            'report_datetime': timezone.now(),
            'delivery_datetime': timezone.now() - relativedelta(days=self.postnatal_enrollment.postpartum_days),
            'delivery_time_estimated': NO,
            'labour_hrs': 6,
            'delivery_hospital': 'PMH',
            'has_uterine_tender': NO,
            'has_temp': NO,
            'labour_max_temp': '',
            'has_chorioamnionitis': NO,
            'delivery_complications': NO,
            'live_infants_to_register': 1,
            'delivery_comment': '',
            'comment': ''
        }

    def test_infants_to_register_1(self):
        form = MaternalLabourDelForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_infants_to_register_2(self):
        '''Cannot register more than 1 infant.'''
        self.data['live_infants_to_register'] = 3
        form = MaternalLabourDelForm(data=self.data)
        self.assertIn('Only one infant per mother can be registered to the study.', form.errors.get('__all__'))

    def test_infants_to_register_3(self):
        '''Infant to register cannot be zero or less'''
        self.data['live_infants_to_register'] = -1
        form = MaternalLabourDelForm(data=self.data)
        self.assertIn('Number of live infants to register may not be less than or equal to 0!.',
                      form.errors.get('__all__'))

    def test_delivery_date_1(self):
        """Delivery date is cannot be greater than reportdate"""
        self.data['report_datetime'] = timezone.now() - timezone.timedelta(days=1)
        self.data['delivery_datetime'] = timezone.now()
        form = MaternalLabourDelForm(data=self.data)
        self.assertIn('Delivery date cannot be greater than the report date. '
                      'Please correct.', form.errors.get('__all__'))

    def test_temp_1(self):
        self.data['has_temp'] = YES
        form = MaternalLabourDelForm(data=self.data)
        self.assertIn("You have indicated that maximum temperature at delivery is known. "
                      "Please provide the maximum temperature.", form.errors.get('__all__'))

    def test_temp_2(self):
        self.data['labour_max_temp'] = 37
        form = MaternalLabourDelForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn("You have indicated that maximum temperature is not known. "
                      "You CANNOT provide the maximum temperature", errors)

    def test_temp_3(self):
        """Temperature cannot be above 37.2"""
        self.data['has_temp'] = YES
        self.data['labour_max_temp'] = 40
        form = MaternalLabourDelForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_temp_4(self):
        form = MaternalLabourDelForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_temp_5(self):
        self.data['has_temp'] = YES
        self.data['labour_max_temp'] = 36.8
        form = MaternalLabourDelForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_deliverydate_vs_postpartum_days(self):
        self.data['delivery_datetime'] = timezone.now() - timezone.timedelta(days=1)
        form = MaternalLabourDelForm(data=self.data)
        self.assertIn('Delivery date does not correspond with the number of days post-partum as '
                      'reported at Postnatal Enrollment. Using \'{}\' days post-partum. Please correct'
                      .format(self.postnatal_enrollment.postpartum_days), form.errors.get('__all__'))


class TestMaternalLabourDelClinic(BaseMaternalTestCase):
    """Test eligibility of a mother for postnatal enrollment."""

    def setUp(self):
        super(TestMaternalLabourDelClinic, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject,
            study_site=self.study_site)
        self.registered_subject = self.maternal_consent.registered_subject
        self.postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            will_breastfeed=YES
        )
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='2000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.labour_del = MaternalLabourDelFactory(maternal_visit=self.maternal_visit)
        self.data = {
            'maternal_visit': self.maternal_visit.id,
            'maternal_lab_del': self.labour_del.id,
            'report_datetime': timezone.now(),
            'has_cd4': NO,
            'cd4_date': '',
            'cd4_result': '',
            'has_vl': NO,
            'vl_date': '',
            'vl_detectable': NOT_APPLICABLE,
            'vl_result': '',
            'comment': ''
        }

    def test_has_cd4_1(self):
        """If has CD4 is indicated as yes, then date CD4 count was performed should be provided."""
        self.data['has_cd4'] = YES
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertIn('You indicated that a CD4 count was performed. Please provide the date.',
                      form.errors.get('__all__'))

    def test_has_cd4_2(self):
        """If has CD4 is indicated as yes, then CD4 count  result should be provided."""
        self.data['has_cd4'] = YES
        self.data['cd4_date'] = timezone.now() - timezone.timedelta(days=2)
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertIn('You indicated that a CD4 count was performed. Please provide the result.',
                      form.errors.get('__all__'))

    def test_has_cd4_3(self):
        """If has CD4 is indicated as no, then CD4 count date should be NOT provided."""
        self.data['has_cd4'] = NO
        self.data['cd4_date'] = timezone.now() - timezone.timedelta(days=2)
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertIn('You indicated that a CD4 count was NOT performed, yet provided a date '
                      'CD4 was performed. Please correct.', form.errors.get('__all__'))

    def test_has_cd4_4(self):
        """If has CD4 is indicated as no, then CD4 count result should be NOT provided."""
        self.data['has_cd4'] = NO
        self.data['cd4_result'] = 600
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertIn('You indicated that a CD4 count was NOT performed, yet provided a CD4 '
                      'result. Please correct.', form.errors.get('__all__'))

    def test_has_cd4_5(self):
        """If has CD4 is indicated as Yes, then CD4 count date and result should be provided."""
        self.data['has_cd4'] = YES
        self.data['cd4_date'] = timezone.now() - timezone.timedelta(days=2)
        self.data['cd4_result'] = 600
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_has_cd4_6(self):
        """If has CD4 is indicated as NO, then CD4 count date and result should be  NOT provided."""
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_has_vl_1(self):
        """If has VL is indicated as yes, then date VL was performed should be provided."""
        self.data['has_vl'] = YES
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertIn('You indicated that a VL count was performed. Please provide the date.',
                      form.errors.get('__all__'))

    def test_has_vl_2(self):
        """If has VL is indicated as yes, then VL result should be provided."""
        self.data['has_vl'] = YES
        self.data['vl_date'] = timezone.now() - timezone.timedelta(days=2)
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertIn('You indicated that a VL count was performed. Please provide the result.',
                      form.errors.get('__all__'))

    def test_has_vl_3(self):
        """If has VL is indicated as NO, then VL date should not be provided."""
        self.data['has_vl'] = NO
        self.data['vl_date'] = timezone.now() - timezone.timedelta(days=2)
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertIn('You indicated that a VL count was NOT performed, yet provided a date VL '
                      'was performed. Please correct.', form.errors.get('__all__'))

    def test_has_vl_4(self):
        """If has VL is indicated as NO, then VL result should not be provided."""
        self.data['has_vl'] = NO
        self.data['vl_result'] = 899
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertIn('You indicated that a VL count was NOT performed, yet provided a VL result'
                      ' Please correct.', form.errors.get('__all__'))

    def test_has_vl_5(self):
        """If has vl is No then VL date and result shot NOT be provided"""
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_has_vl_6(self):
        self.data['has_vl'] = YES
        self.data['vl_date'] = timezone.now() - timezone.timedelta(days=2)
        self.data['vl_result'] = 1389
        form = MaternalLabDelClinicForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'You stated that a VL count was performed. Please indicate if it was detectable.', errors)

    def test_has_vl_7(self):
        """If has VL  is YES, the both VL date and result should be provided"""
        self.data['has_vl'] = YES
        self.data['vl_date'] = timezone.now() - timezone.timedelta(days=2)
        self.data['vl_detectable'] = YES
        self.data['vl_result'] = 1389
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_has_vl_8(self):
        self.data['has_vl'] = NO
        self.data['vl_detectable'] = YES
        form = MaternalLabDelClinicForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'You stated that a VL count was NOT performed, you CANNOT indicate if VL was detectable.',
            errors)
