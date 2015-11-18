from django.test import TestCase
from django.utils import timezone

from edc.core.bhp_variables.tests.factories.study_site_factory import StudySiteFactory
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc_constants.choices import YES, NO

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from bhp077.apps.microbiome_maternal.forms import (MaternalLabourDelForm, MaternalLabDelClinicForm,
                                                   MaternalLabDelMedForm)

from ..visit_schedule import PostnatalEnrollmentVisitSchedule
from .factories import (PostnatalEnrollmentFactory, MaternalLabourDelFactory, MaternalVisitFactory,
                        MaternalEligibilityFactory, MaternalConsentFactory)
from bhp077.apps.microbiome_list.models.maternal_lab_del import HealthCond


class TestMaternalLabourDel(TestCase):
    """Test eligibility of a mother for postnatal enrollment."""

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()
        self.study_site = StudySiteFactory(site_code='10', site_name='Gabs')
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject,
                                                       study_site=self.study_site)
        self.registered_subject = self.maternal_consent.registered_subject
        self.postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            breastfeed_for_a_year=YES
        )
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='2000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.data = {
            'maternal_visit': self.maternal_visit.id,
            'report_datetime': timezone.now(),
            'delivery_datetime': timezone.now() - timezone.timedelta(days=1),
            'del_time_is_est': NO,
            'labour_hrs': 6,
            'del_hosp': 'PMH',
            'has_uterine_tender': NO,
            'labr_max_temp': -1,
            'has_chorioamnionitis': NO,
            'has_del_comp': NO,
            'live_infants_to_register': 1,
            'del_comment': '',
            'comment': ''
        }

    def test_infants_to_register_1(self):
        '''Cannot register more than 1 infant.'''
        self.data['live_infants_to_register'] = 3
        form = MaternalLabourDelForm(data=self.data)
        self.assertIn(u'For this study we can only register ONE infant', form.errors.get('__all__'))

    def test_infants_to_register_2(self):
        form = MaternalLabourDelForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_infants_to_register_3(self):
        '''Infant to register cannot be zero or less'''
        self.data['live_infants_to_register'] = -1
        form = MaternalLabourDelForm(data=self.data)
        self.assertIn(u'Number of live infants to register may not be less than or equal to 0!.',
                      form.errors.get('__all__'))

    def test_delivery_date_1(self):
        """Delivery date is cannot be greater than reportdate"""
        self.data['report_datetime'] = timezone.now() - timezone.timedelta(days=1)
        self.data['delivery_datetime'] = timezone.now()
        form = MaternalLabourDelForm(data=self.data)
        self.assertIn(u'Maternal Labour Delivery date cannot be greater than report date. '
                      'Please correct.', form.errors.get('__all__'))


class TestMaternalLabourDelClinic(TestCase):
    """Test eligibility of a mother for postnatal enrollment."""

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()
        self.study_site = StudySiteFactory(site_code='10', site_name='Gabs')
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject,
                                                       study_site=self.study_site)
        self.registered_subject = self.maternal_consent.registered_subject
        self.postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            breastfeed_for_a_year=YES
        )
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
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
            'vl_result': '',
            'comment': ''
        }

    def test_has_cd4_1(self):
        """If has CD4 is indicated as yes, then date CD4 count was performed should be provided."""
        self.data['has_cd4'] = YES
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertIn(u'You indicated that a CD4 count was performed. Please provide the date.',
                      form.errors.get('__all__'))

    def test_has_cd4_2(self):
        """If has CD4 is indicated as yes, then CD4 count  result should be provided."""
        self.data['has_cd4'] = YES
        self.data['cd4_date'] = timezone.now() - timezone.timedelta(days=2)
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertIn(u'You indicated that a CD4 count was performed. Please provide the result.',
                      form.errors.get('__all__'))

    def test_has_cd4_3(self):
        """If has CD4 is indicated as no, then CD4 count date should be NOT provided."""
        self.data['has_cd4'] = NO
        self.data['cd4_date'] = timezone.now() - timezone.timedelta(days=2)
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertIn(u'You indicated that a CD4 count was NOT performed, yet provided a date '
                      'CD4 was performed. Please correct.', form.errors.get('__all__'))

    def test_has_cd4_4(self):
        """If has CD4 is indicated as no, then CD4 count result should be NOT provided."""
        self.data['has_cd4'] = NO
        self.data['cd4_result'] = 600
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertIn(u'You indicated that a CD4 count was NOT performed, yet provided a CD4 '
                      'result. Please correct.', form.errors.get('__all__'))

    def test_has_cd4_5(self):
        """If has CD4 is indicated as Yes, then CD4 count date and result should be provided."""
        self.data['has_cd4'] = YES
        self.data['cd4_date'] = timezone.now() - timezone.timedelta(days=2)
        self.data['cd4_result'] = 600
        form = MaternalLabDelClinicForm(data=self.data)
        print form.errors
        self.assertTrue(form.is_valid())

    def test_has_cd4_6(self):
        """If has CD4 is indicated as NO, then CD4 count date and result should be  NOT provided."""
        form = MaternalLabDelClinicForm(data=self.data)
        print form.errors
        self.assertTrue(form.is_valid())

    def test_has_vl_1(self):
        """If has VL is indicated as yes, then date VL was performed should be provided."""
        self.data['has_vl'] = YES
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertIn(u'You indicated that a VL count was performed. Please provide the date.',
                      form.errors.get('__all__'))

    def test_has_vl_2(self):
        """If has VL is indicated as yes, then VL result should be provided."""
        self.data['has_vl'] = YES
        self.data['vl_date'] = timezone.now() - timezone.timedelta(days=2)
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertIn(u'You indicated that a VL count was performed. Please provide the result.',
                      form.errors.get('__all__'))

    def test_has_vl_3(self):
        """If has VL is indicated as NO, then VL date should not be provided."""
        self.data['has_vl'] = NO
        self.data['vl_date'] = timezone.now() - timezone.timedelta(days=2)
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertIn(u'You indicated that a VL count was NOT performed, yet provided a date VL '
                      'was performed. Please correct.', form.errors.get('__all__'))

    def test_has_vl_4(self):
        """If has VL is indicated as NO, then VL result should not be provided."""
        self.data['has_vl'] = NO
        self.data['vl_result'] = 899
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertIn(u'You indicated that a VL count was NOT performed, yet provided a VL result'
                      ' Please correct.', form.errors.get('__all__'))

    def test_has_vl_5(self):
        """If has vl is No then VL date and result shot NOT be provided"""
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_has_vl_6(self):
        """If has VL  is YES, the both VL date and result should be provided"""
        self.data['has_vl'] = YES
        self.data['vl_date'] = timezone.now() - timezone.timedelta(days=2)
        self.data['vl_result'] = 1389
        form = MaternalLabDelClinicForm(data=self.data)
        self.assertTrue(form.is_valid())


class TestMaternalLabourMed(TestCase):
    """Test eligibility of a mother for postnatal enrollment."""

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()
        self.study_site = StudySiteFactory(site_code='10', site_name='Gabs')
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject,
                                                       study_site=self.study_site)
        self.registered_subject = self.maternal_consent.registered_subject
        self.postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            breastfeed_for_a_year=YES
        )
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='2000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.labour_del = MaternalLabourDelFactory(maternal_visit=self.maternal_visit)
        self.health_cond = HealthCond.objects.create(name='N/A', short_name='N/A', display_index=10, field_name='health_cond')
        self.data = {
            'maternal_visit': self.maternal_visit.id,
            'report_datetime': timezone.now(),
            'has_health_cond': NO,
            'health_cond': self.health_cond.id,
            'has_ob_comp': NO,
            'ob_comp': 'N/A',
            'ob_comp_other': '',
            'took_suppliments': NO,
            'suppliments': 'N/A',
            'comment': '',
        }

    def test_has_health_cond(self):
        self.data['has_health_cond'] = YES
        form = MaternalLabDelMedForm(data=self.data)
        print form.errors
