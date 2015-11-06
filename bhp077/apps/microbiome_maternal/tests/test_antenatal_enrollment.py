from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc_constants.choices import POS, YES

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_maternal.tests.factories import AntenatalEnrollmentFactory
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from ..visit_schedule import AntenatalEnrollmentVisitSchedule


class TestAntenatalEnroll(TestCase):
    """Test eligibility of a mother for antenatal enrollment."""

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        AntenatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()

    def test_eligibility_for_correct_age(self):
        """Test for a positive mother on a valid regimen."""

        antenatal_enrollment = AntenatalEnrollmentFactory(verbal_hiv_status=POS, evidence_hiv_status=YES)
        self.assertTrue(antenatal_enrollment.eligible_for_postnatal)
