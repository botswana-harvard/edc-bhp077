from django.test import TestCase

from ...microbiome_maternal.models import AntenatalEnrollment
from ...microbiome_maternal.tests.factories import AntenatalEnrollmentFactory

from ..views import GenerateCallList
from ..models import AntenatalCallList

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from ...microbiome_maternal.tests.factories import (MaternalConsentFactory, SampleConsentFactory,
                                                    MaternalEligibilityFactory)
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from ...microbiome_maternal.visit_schedule import AntenatalEnrollmentVisitSchedule


class TestGenerateCallList(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        AntenatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject
        SampleConsentFactory(registered_subject=self.registered_subject)

    def test_generate_call_list(self):
        """Test create call log."""
        AntenatalEnrollmentFactory(weeks_of_gestation=32, registered_subject=self.registered_subject)
        GenerateCallList().create_antenatal_call_list()
        antenatal_enrollment = AntenatalEnrollment.objects.all().count()
        self.assertEqual(antenatal_enrollment, 1)
        self.assertEqual(AntenatalCallList.objects.all().count(), 1)
