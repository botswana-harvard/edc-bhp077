from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc_constants.constants import POS, YES, NO, NEG, NOT_APPLICABLE

from microbiome.apps.mb.app_configuration.classes import MicrobiomeConfiguration
from microbiome.apps.mb_maternal.tests.factories import (
    AntenatalEnrollmentFactory, MaternalEligibilityFactory, PostnatalEnrollmentFactory)
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory
from microbiome.apps.mb_lab.lab_profiles import MaternalProfile
from ..visit_schedule import AntenatalEnrollmentVisitSchedule
from edc_offstudy.models.off_study_model_mixin import OffStudyError


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
            rapid_test_done=NOT_APPLICABLE,
            registered_subject=self.registered_subject,
            gestation_wks=35)
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_if_antenatal_postnatal_eligible(self):

        AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            registered_subject=self.registered_subject,
            gestation_wks=36)

        postnatal_enrollment = PostnatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            registered_subject=self.registered_subject,
            gestation_wks_delivered=38)

        self.assertTrue(postnatal_enrollment.is_eligible)

    def test_if_antenatal_postnatal_not_eligible(self):
        """Asserts raises exception if antenatal enrollment is not eligible and an attempt
        is made to complete postnatal enrollment."""
        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            week32_test=NO,
            rapid_test_done=NOT_APPLICABLE,
            registered_subject=self.registered_subject,
            gestation_wks=35)
        self.assertFalse(antenatal_enrollment.is_eligible)
        with self.assertRaises(OffStudyError):
            PostnatalEnrollmentFactory(
                current_hiv_status=POS,
                evidence_hiv_status=YES,
                rapid_test_done=NOT_APPLICABLE,
                registered_subject=self.registered_subject,
                gestation_wks_delivered=38,
                will_remain_onstudy=NO)

    def test_if_antenatal_not_eligible(self):
        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            registered_subject=self.registered_subject,
            gestation_wks=35,
            will_remain_onstudy=NO,
            is_diabetic=YES)
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_antenatal_ineligible_if_gestation_not_36_pos(self):
        """
            current_hiv_status = ?
            evidence_hiv_status = ?

            on_hypertension_tx = NO
            is_diabetic = NO
            on_tb_tx = NO
            will_breastfeed = YES
            will_remain_onstudy = YES

            valid_regimen = YES
            valid_regimen_duration = YES
            week32_test = YES
            week32_result = POS
        """

        antenatal_enrollment = AntenatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            gestation_wks=35,
            week32_test=YES,
            week32_result=POS)
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_antenatal_eligible_if_gestation_36_pos1(self):
        """Assert eligible if POS by week32 test, current, evidence."""
        antenatal_enrollment = AntenatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            gestation_wks=36,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            week32_test=YES,
            week32_result=POS)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_antenatal_eligible_if_gestation_36_pos2(self):
        """Assert eligible if POS by week32 test."""
        antenatal_enrollment = AntenatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            gestation_wks=36,
            rapid_test_done=NOT_APPLICABLE,
            week32_test=YES,
            week32_result=POS)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_antenatal_not_eligible_if_gestation_not_36_neg(self):
        antenatal_enrollment = AntenatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            gestation_wks=35,
            week32_test=YES,
            week32_result=NEG,
            rapid_test_done=NOT_APPLICABLE,
            current_hiv_status=POS,
            evidence_hiv_status=YES)
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_antenatal_eligible_if_gestation_36_neg(self):
        antenatal_enrollment = AntenatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            gestation_wks=36,
            week32_test=YES,
            week32_result=NEG,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_if_postnatal_not_eligible(self):
        postnatal_enrollment = PostnatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            registered_subject=self.registered_subject,
            gestation_wks_delivered=35,
            will_remain_onstudy=NO)
        self.assertFalse(postnatal_enrollment.is_eligible)

    def test_if_postnatal_eligible(self):
        postnatal_enrollment = PostnatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            registered_subject=self.registered_subject,
            gestation_wks_delivered=35,
        )
        self.assertFalse(postnatal_enrollment.is_eligible)
