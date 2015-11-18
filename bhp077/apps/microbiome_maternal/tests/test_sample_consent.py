from django.test import TestCase
from django.utils import timezone

from edc.core.bhp_variables.tests.factories.study_site_factory import StudySiteFactory
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc_constants.choices import YES, NO

from .factories import (MaternalEligibilityFactory, MaternalConsentFactory, SampleConsentFactory)

from ..visit_schedule import PostnatalEnrollmentVisitSchedule
from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from bhp077.apps.microbiome_maternal.models import MaternalConsent, SampleConsent


class TestSampleConsent(TestCase):
    """Test sample consent vs similarities in maternal consent"""

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()
        self.study_site = StudySiteFactory(site_code='40', site_name='Gaborone')
        self.maternal_eligibility = MaternalEligibilityFactory()

        primary_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject,
                                                 study_site=self.study_site)

        sample_consent = SampleConsentFactory(registered_subject=primary_consent.registered_subject)

        def test_one_consent_one_sample(self):
            self.assertEqual(MaternalConsent.objects.all().count(), 1)
            self.assertEqual(SampleConsent.objects.all().count(), 1)

        def test_consents_subject_identifier(self):
            print ('Assert Subject Identifiers are same')
            self.assertEqual(primary_consent.registered_subject.subject_identifier, sample_consent.registered_subject.subject_identifier)

        def test_consents_is_literate(self):
            print ('Assert literacy')
            self.assertEqual(primary_consent.is_literate, sample_consent.is_literate)

        def test_consents_witness_name(self):
            print ('Assert Witness names are same')
            eligibility1 = MaternalEligibilityFactory()
            consent1 = MaternalConsentFactory(registered_subject=eligibility1.registered_subject,
                                              study_site=self.study_site, is_literate=NO,
                                              witness_name='DIDI, JAYDEN')
            consent2 = SampleConsentFactory(registered_subject=consent1.registered_subject,
                                            is_literate=NO, witness_name='DIDI, JAYDEN')
            self.assertEqual(consent1.witness_name, consent2.witness_name)
