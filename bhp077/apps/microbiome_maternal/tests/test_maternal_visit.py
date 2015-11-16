import datetime

from django.test import TestCase
from django.utils import timezone

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.subject.appointment.models import Appointment
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc_constants.choices import YES, NO, POS, NEG, NOT_APPLICABLE

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_maternal.tests.factories import MaternalEligibilityFactory
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory
from bhp077.apps.microbiome_maternal.models import MaternalVisit
from bhp077.apps.microbiome_maternal.forms import MaternalVisitForm
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from ..visit_schedule import PostnatalEnrollmentVisitSchedule
from .factories import PostnatalEnrollmentFactory
from bhp077.apps.microbiome_maternal.tests.factories.maternal_visit_factory import MaternalVisitFactory
from edc.core.bhp_variables.tests.factories.study_site_factory import StudySiteFactory
from edc.subject.appointment.tests.factories.appointment_factory import AppointmentFactory


class TestMaternalVisit(TestCase):
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
        self.data = {
            'appointment': self.appointment.id,
            'report_datetime': timezone.now(),
            'info_source': 'participant',
            'info_source_other': '',
            'reason': 'scheduled',
            'reason_unscheduled': '',
            'reason_missed': '',
            'comments': '',
        }

    def test_reason_unscheduled(self):
        self.data['reason'] = 'unscheduled'
        form = MaternalVisitForm(data=self.data)
        self.assertIn(u'You indicated that this is an unscheduled visit. Please '
                      'provide a reason for the unscheduled visit.', form.errors.get('__all__'))

    def test_reason_not_unscheduled(self):
        self.data['reason_unscheduled'] = 'Patient called'
        form = MaternalVisitForm(data=self.data)
        self.assertIn(u'You indicated that this is NOT an unscheduled visit, yet provided a '
                      'reason why it is unscheduled. Please correct.', form.errors.get('__all__'))

    def test_missed_visit_no_reason(self):
        self.data['reason'] = 'missed'
        form = MaternalVisitForm(data=self.data)
        self.assertIn(u'You indicated that the visit was missed. Please provide a reason why '
                      'it was missed.', form.errors.get('__all__'))

    def test_attended_visit_reason_missed_given(self):
        self.data['reason_missed'] = 'Shopping'
        form = MaternalVisitForm(data=self.data)
        self.assertIn(u'You indicated that the visit was NOT missed, yet you provided a reason '
                      'why it was missed. Please correct.', form.errors.get('__all__'))

    def test_missed_visit_info_source_1(self):
        """If visit is missed, no information source provider should be provided"""
        self.data['reason'] = 'missed'
        self.data['reason_missed'] = 'Shopping'
        self.data['info_source'] = ''
        form = MaternalVisitForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_missed_visit_info_source_2(self):
        """If visit is missed, Information source should not be provided"""
        self.data['reason'] = 'missed'
        self.data['reason_missed'] = 'Shopping'
        self.data['info_source'] = 'participant'
        form = MaternalVisitForm(data=self.data)
        self.assertIn(u'You have indicated that the visit was missed. '
                      'Please do not provide source of information.', form.errors.get('__all__'))

    def test_missed_visit_info_source_3(self):
        """If visit is NOT missed, Information source should be provided"""
        self.data['reason'] = 'reason'
        self.data['info_source'] = ''
        form = MaternalVisitForm(data=self.data)
        self.assertIn(u'You indicated that the visit was NOT missed. '
                      'Please provide source of information.', form.errors.get('__all__'))
