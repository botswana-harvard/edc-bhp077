from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_maternal.tests.factories import MaternalEligibilityFactory
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from ..visit_schedule import AntenatalEnrollmentVisitSchedule


class TestMaternalConsent(TestCase):
    """Test maternal consent."""

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        AntenatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()

    def test_martenal_consent_identity(self):
        """Test identity duplication."""

        maternal_eligibility1 = MaternalEligibilityFactory()
        MaternalConsentFactory(
            registered_subject=maternal_eligibility1.registered_subject,
            identity="111121111",
            identity_type="Omang",
            confirm_identity="111121111"
        )

        maternal_eligibility2 = MaternalEligibilityFactory()
        MaternalConsentFactory(
            registered_subject=maternal_eligibility2.registered_subject,
            identity="111121111",
            identity_type="Omang",
            confirm_identity="111121111"
        )
