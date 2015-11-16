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
from bhp077.apps.microbiome_maternal.forms import MaternalLabourDelForm
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory
from bhp077.apps.microbiome_maternal.tests.factories import MaternalEligibilityFactory

from ..visit_schedule import PostnatalEnrollmentVisitSchedule
from .factories import PostnatalEnrollmentFactory
from bhp077.apps.microbiome_maternal.tests.factories.maternal_visit_factory import MaternalVisitFactory


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
