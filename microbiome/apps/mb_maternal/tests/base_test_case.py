from django.test.testcases import TestCase

from edc_rule_groups.classes.controller import site_rule_groups
from edc_lab.lab_profile.classes.controller import site_lab_profiles
from edc_lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile

from microbiome.apps.mb_lab.lab_profiles import MaternalProfile
from microbiome.apps.mb.app_configuration import AppConfiguration
from microbiome.apps.mb_maternal.visit_schedule import (
    SpecimenConsentVisitSchedule, AntenatalEnrollmentVisitSchedule, PostnatalEnrollmentVisitSchedule)


class BaseMaternalTestCase(TestCase):
    """Test eligibility of a mother for antenatal enrollment."""

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        AppConfiguration(lab_profiles=site_lab_profiles).prepare()
        SpecimenConsentVisitSchedule().build()
        AntenatalEnrollmentVisitSchedule().build()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()
        self.study_site = '40'
