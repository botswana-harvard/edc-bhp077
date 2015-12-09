from django import forms
from django.test import TestCase
from django.utils import timezone

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc_constants.constants import POS, YES, NO, NEG, NOT_APPLICABLE, UNKNOWN

from bhp077.apps.microbiome_maternal.models import AntenatalEnrollment
from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_maternal.tests.factories import (AntenatalEnrollmentFactory, MaternalEligibilityFactory, PostnatalEnrollmentFactory)
from bhp077.apps.microbiome_maternal.tests.factories import MaternalConsentFactory
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
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject
        self.data = {
            'registered_subject': self.registered_subject}

    def test_gestation_wks_below_36(self):
        """Test for a positive mother with evidence of hiv_status,
        on a valid regimen but weeks of gestation period below 36."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            gestation_wks=35
        )
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_gestation_wks_above_36_and_no_regimen(self):
        """Test for a positive mother with evidence of hiv_status,
        not on a valid regimen but weeks of gestation period above 36."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            valid_regimen=NO,
            registered_subject=self.registered_subject,
            gestation_wks=37
        )
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_is_diabetic(self):
        """Test for a positive mother with valid documentation,
        on a valid regimen but is diabetic."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            is_diabetic=YES
        )
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_is_not_diabetic(self):
        """Test for a positive mother with valid documentation,
        on a valid regimen but not diabetic."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            is_diabetic=NO
        )
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_has_hyptertension(self):
        """Test for a positive mother with valid documentation,
        on a valid regimen and has hypertension."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            on_hypertension_tx=YES
        )
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_has_no_hyptertension(self):
        """Test for a positive mother with documentation evidence,
        on a valid regimen and not hypertensive."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            on_hypertension_tx=NO
        )
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_will_breastfeed(self):
        """Test for a negative mother with documentation evidence,
        amd who agrees to breastfeed for a year."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            will_breastfeed=YES
        )
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_no_will_breastfeed(self):
        """Test for a negative mother who has documentation of hiv_status,
        but does not agree to breastfeed for a year."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            will_breastfeed=NO
        )
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_will_remain_onstudy(self):
        """Test for a negative mother who has documenation of hiv_status,
        and agrees to stay in study a year."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            will_remain_onstudy=YES
        )
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_not_will_remain_onstudy(self):
        """Test for a negative mother who has documentatin of hiv_status,
        but does not agree to stay in study for a year."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            will_remain_onstudy=NO
        )
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_positive_with_evidence(self):
        """Test for a negative mother with evidence."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
        )
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_positive_with_no_evidence_and_rapid_test_done(self):
        """Test for a negative mother who has no documentation of hiv_status,
        but no rapid test done."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=NO,
            registered_subject=self.registered_subject,
            rapid_test_done=NO,
        )
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_positive_with_no_evidence_and_gestation_37(self):
        """Test for a positive mother with no hiv_status documentation,
        and no rapid test done but gestation at 37 weeks."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            current_hiv_status=POS,
            evidence_hiv_status=NO,
            registered_subject=self.registered_subject,
            rapid_test_done=NO,
            gestation_wks=37,
        )
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_fail_fill_antenatal_if_postnatal_filled(self):
        """Test that if postnatal already exists, filling of antenatal fails."""
        PostnatalEnrollmentFactory(registered_subject=self.registered_subject)
        AntenatalEnrollmentFactory(registered_subject=self.registered_subject)
        self.assertRaises(forms.ValidationError)

    def test_cannot_change_rapid_test_date(self):
        """Test that rapid test date cannot be changed after first entry at enrollment"""
        antenatal = AntenatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=NO,
            valid_regimen=NOT_APPLICABLE,
            valid_regimen_duration=NOT_APPLICABLE,
            rapid_test_done=YES,
            rapid_test_date=timezone.now().date() - timezone.timedelta(days=1),
            rapid_test_result=POS)
        self.assertTrue(AntenatalEnrollment.objects.count(), 1)
        antenatal.rapid_test_date = timezone.now().date()
        antenatal.save()
        self.assertRaises(forms.ValidationError)

    def test_mother_tested_at_32weeks_with_evidence(self):
        """Test for a positive mother who tested at 32weeks,
        and has documentation of hiv_status with gestational age at 37weeks"""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            week32_test=YES,
            week32_result=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            gestation_wks=37
        )
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_mother_tested_at_32weeks_without_evidence(self):
        """Test for a mother who is at 37weeks of gestational age,
        tested at 32weeks, but has no evidence of the hiv_status but undergoes rapid testing """

        antenatal_enrollment = AntenatalEnrollmentFactory(
            week32_test=YES,
            week32_result=None,
            current_hiv_status=NEG,
            evidence_hiv_status=NO,
            rapid_test_done=YES,
            registered_subject=self.registered_subject,
            gestation_wks=37
        )
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_no_week32test_no_rapid_test(self):
        """Test for a mother who is at 37weeks gestational age,
        did not test at week 32 and does not do a rapid test"""
        antenatal_enrollment = AntenatalEnrollmentFactory(
            week32_test=NO,
            week32_result=None,
            evidence_hiv_status=NO,
            rapid_test_done=NO,
            registered_subject=self.registered_subject,
            gestation_wks=37
        )
        self.assertFalse(antenatal_enrollment.is_eligible)

    def test_no_week32test_does_rapid_test(self):
        """Test for a mother at 37weeks gestational age,
        who did not do hiv_testing at 32weeks but undergoes rapid testing"""
        antenatal_enrollment = AntenatalEnrollmentFactory(
            week32_test=NO,
            week32_result='',
            rapid_test_done=YES,
            registered_subject=self.registered_subject,
            gestation_wks=37
        )
        self.assertTrue(antenatal_enrollment.is_eligible)

    def test_no_week32test_evidence_na(self):
        """Test for a mother who has eligible gestational weeks, who is
        not aware of current hiv_status but undergoes rapid testing """
        antenatal_enrollment = AntenatalEnrollmentFactory(
            week32_test=NO,
            week32_result='',
            evidence_hiv_status=NOT_APPLICABLE,
            valid_regimen=NOT_APPLICABLE,
            valid_regimen_duration=NOT_APPLICABLE,
            current_hiv_status=UNKNOWN,
            rapid_test_done=YES,
            registered_subject=self.registered_subject,
            gestation_wks=37
        )
        self.assertTrue(antenatal_enrollment.is_eligible)
