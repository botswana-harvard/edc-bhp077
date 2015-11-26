from django.test import TestCase
from django.utils import timezone

from edc.core.bhp_variables.tests.factories.study_site_factory import StudySiteFactory
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.subject.code_lists.models import WcsDxAdult
from edc_constants.choices import YES, NO

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from bhp077.apps.microbiome_list.models.chronic_conditions import ChronicConditions
from bhp077.apps.microbiome_maternal.forms import (MaternalArvPostForm, MaternalArvPregForm)

from ..visit_schedule import PostnatalEnrollmentVisitSchedule
from .factories import (PostnatalEnrollmentFactory, MaternalVisitFactory,
                        MaternalEligibilityFactory, MaternalConsentFactory)


class TestMaternalArvPost(TestCase):
    """Test eligibility of a mother for ARV."""

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
            'haart_last_visit': NO,
            'haart_reason': 'N/A',
            'haart_reason_other': '',
            'arv_status': 'N/A',
        }

    def test_on_haart_1(self):
        """Assert that if mother was supposed to take HAART, then reason for haart cannot be N/A"""
        self.data['haart_last_visit'] = YES
        form = MaternalArvPostForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(u"You indicated that participant was on HAART. Reason CANNOT be 'Not Applicable'. ", errors)

    def test_on_haart_2(self):
        """Assert that if mother was not supposed to take HAART, then cannot provide a reason for taking HAART"""
        self.data['haart_reason'] = 'pmtct bf'
        form = MaternalArvPostForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(u'You indicated that participant was not on HAART. You CANNOT provide a reason.', errors)

    def test_on_haart_3(self):
        """Assert that mother was not supposed to take HAART and no reason for taking HAART is provided then valid"""
        form = MaternalArvPostForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_on_haart_4(self):
        """Assert that if mother was supposed to take HAART, and reason for HAART given is valid"""
        self.data['haart_last_visit'] = YES
        self.data['haart_reason'] = 'pmtct bf'
        form = MaternalArvPostForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_tooke_arv_5(self):
        """Assert that ARV indicated as not interrupted, then reason not expected"""
        self.data['interrupt'] = 'FORGOT'
        self.data['took_arv'] = NO
        self.postnatal_enrollment.valid_regimen_duration = YES
        self.postnatal_enrollment.save()
        form = MaternalArvPregForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(u'You indicated that the participant has been on regimen for period of time. The answer should '
                      u'be (YES)to question 3.(ARVs during pregnancy?).', errors)


class TestMaternalArvPreg(TestCase):
    """Test eligibility of a mother for ARV Preg."""

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
            breastfeed_for_a_year=YES,
        )
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject,
                                                   visit_definition__code='2000M')
        self.maternal_visit = MaternalVisitFactory(appointment=self.appointment)
        self.data = {
            'maternal_visit': self.maternal_visit.id,
            'report_datetime': timezone.now(),
            'took_arv': NO,
            'is_interrupt': NO,
            'interrupt': 'N/A',
            'interrupt_other': '',
            'comment': '',
        }

    def test_tooke_arv_1(self):
        """Assert that ARV indicated as interrupted, then reason expected"""
        self.data['is_interrupt'] = YES
        form = MaternalArvPregForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(u'You indicated that ARVs were interrupted during pregnancy. '
                      'Please provide a reason', errors)

    def test_tooke_arv_2(self):
        """Assert that ARV indicated as not interrupted, then reason not expected"""
        self.data['interrupt'] = 'FORGOT'
        form = MaternalArvPregForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(u'You indicated that ARVs were NOT interrupted during pregnancy. '
                      'You cannot provide a reason.', errors)

#     def test_tooke_arv_3(self):
#         """Assert that ARV indicated as interrupted, and reason provided, then valid"""
#         self.data['is_interrupt'] = YES
#         self.data['interrupt'] = 'NO_REFILL'
#         form = MaternalArvPregForm(data=self.data)
#         self.assertTrue(form.is_valid())
# 
#     def test_tooke_arv_4(self):
#         """Assert that ARV indicated as uninterrupted, and reason not provided, then valid"""
#         form = MaternalArvPregForm(data=self.data)
#         self.assertTrue(form.is_valid())
