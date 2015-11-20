from django.test import TestCase
from django.utils import timezone

from edc.core.bhp_variables.tests.factories.study_site_factory import StudySiteFactory
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc_constants.choices import YES

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from bhp077.apps.microbiome_maternal.forms import MaternalVisitForm
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory
from bhp077.apps.microbiome_maternal.tests.factories import MaternalEligibilityFactory

from ..visit_schedule import PostnatalEnrollmentVisitSchedule
from .factories import PostnatalEnrollmentFactory


class TestMaternalVisit(TestCase):
    """Test eligibility of a mother for maternal visit."""

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
        self.data = {
            'appointment': self.appointment.id,
            'report_datetime': timezone.now(),
            'info_source': 'participant',
            'info_source_other': '',
            'reason': '',
            'reason_missed': '',
            'comments': '',
        }

    def test_reason_missed(self):
        self.data['reason'] = 'missed'
        form = MaternalVisitForm(data=self.data)
        self.assertIn(u'You indicated that this is a missed visit. Please provide reason missed', form.errors.get('__all__'))

    def test_reason_not_missed(self):
        self.data['reason'] = 'scheduled'
        self.data['reason_missed'] = 'Patient held up'
        form = MaternalVisitForm(data=self.data)
        self.assertIn(u'You indicated that this is NOT a missed visit, yet provided a '
                      'reason why it is missed. Please correct.', form.errors.get('__all__'))

    def test_reason_missed_info_source_given(self):
        self.data['reason'] = 'missed'
        self.data['reason_missed'] = 'Patient held up'
        form = MaternalVisitForm(data=self.data)
        self.assertIn(u'You have indicated that the visit was missed. Please do not provide'
                      ' source of information.', form.errors.get('__all__'))

    def test_reason_not_missed_info_not_given(self):
        self.data['reason'] = 'scheduled'
        self.data['info_source'] = ''
        form = MaternalVisitForm(data=self.data)
        self.assertIn(u'You indicated that the visit was NOT missed. Please provide source of'
                      ' information.', form.errors.get('__all__'))
