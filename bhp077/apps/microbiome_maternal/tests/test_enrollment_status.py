from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc_constants.constants import POS, YES, NO

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_maternal.tests.factories import (AntenatalEnrollmentFactory, MaternalEligibilityFactory, PostnatalEnrollmentFactory)
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from ..visit_schedule import AntenatalEnrollmentVisitSchedule


class TestEnrollmentStatus(TestCase):

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
        self.data = {
            'registered_subject': self.registered_subject}

    def test_gestation_wks_below_36(self):
        """Test for a positive mother on a valid regimen but weeks of gestation below 36."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            gestation_wks=35)
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_if_antenatal_postnatal_eligible(self):

        AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            gestation_wks=35)

        postnatal_enrollment = PostnatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            gestation_wks_delivered=35)

        self.assertTrue(postnatal_enrollment.is_eligible)

    def test_if_antenatal_postnatal_not_eligible(self):

        AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            gestation_wks=35)

        postnatal_enrollment = PostnatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            gestation_wks_delivered=35,
            will_remain_onstudy=NO)

        self.assertTrue(postnatal_enrollment.is_eligible)

    def test_if_antenatal_not_eligible(self):
        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            gestation_wks=35,
            will_remain_onstudy=NO,
            is_diabetic=YES)
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_if_antenatal_eligible(self):
        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            gestation_wks=35)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_if_postnatal_not_eligible(self):
        postnatal_enrollment = PostnatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            gestation_wks_delivered=35,
            will_remain_onstudy=NO)
        self.assertFalse(postnatal_enrollment.is_eligible)

    def test_if_postnatal_eligible(self):
        postnatal_enrollment = PostnatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            gestation_wks_delivered=35,
        )
        self.assertFalse(postnatal_enrollment.is_eligible)
