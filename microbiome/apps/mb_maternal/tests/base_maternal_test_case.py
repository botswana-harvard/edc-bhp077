from django.test.testcases import TestCase

from edc.core.bhp_variables.models import StudySite
from edc.subject.rule_groups.classes.controller import site_rule_groups
from edc.subject.lab_tracker.classes.controller import site_lab_tracker
from edc.lab.lab_profile.classes.controller import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile

from microbiome.apps.mb_lab.lab_profiles import MaternalProfile
from microbiome.apps.mb.app_configuration.classes import MicrobiomeConfiguration
from microbiome.apps.mb_maternal.visit_schedule import (
    SpecimenConsentVisitSchedule, AntenatalEnrollmentVisitSchedule, PostnatalEnrollmentVisitSchedule)


class BaseMaternalTestCase(TestCase):
    """Test eligibility of a mother for antenatal enrollment."""

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        SpecimenConsentVisitSchedule().build()
        AntenatalEnrollmentVisitSchedule().build()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()
        self.study_site = StudySite.objects.first()
