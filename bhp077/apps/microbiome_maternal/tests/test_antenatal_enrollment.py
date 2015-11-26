from django import forms
from django.test import TestCase
from django.utils import timezone

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc_constants.constants import POS, YES, NO, NEG, NOT_APPLICABLE

from bhp077.apps.microbiome_maternal.models import AntenatalEnrollment
from bhp077.apps.microbiome_maternal.forms import AntenatalEnrollmentForm
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

    def test_weeks_of_gestation_below_36(self):
        """Test for a positive mother on a valid regimen but weeks of gestation below 36."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            verbal_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            weeks_of_gestation=35
        )
        self.assertFalse(antenatal_enrollment.eligible_for_postnatal)

    def test_weeks_of_gestation_above_36_and_no_regimen(self):
        """Test for a positive mother not on a valid regimen but weeks of gestation above 36."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            verbal_hiv_status=POS,
            evidence_hiv_status=YES,
            valid_regimen=NO,
            registered_subject=self.registered_subject,
            weeks_of_gestation=37
        )
        self.assertFalse(antenatal_enrollment.eligible_for_postnatal)

    def test_is_diabetic(self):
        """Test for a positive mother on a valid regimen and a diabetic subject."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            verbal_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            is_diabetic=YES
        )
        self.assertFalse(antenatal_enrollment.eligible_for_postnatal)

    def test_is_not_diabetic(self):
        """Test for a positive mother on a valid regimen and a diabetic subject."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            verbal_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            is_diabetic=NO
        )
        self.assertTrue(antenatal_enrollment.eligible_for_postnatal)

    def test_has_hyptertension(self):
        """Test for a positive mother on a valid regimen and has hypertension."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            verbal_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            on_hypertension_treatment=YES
        )
        self.assertFalse(antenatal_enrollment.eligible_for_postnatal)

    def test_has_no_hyptertension(self):
        """Test for a positive mother on a valid regimen and not hypertensive."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            verbal_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            on_hypertension_treatment=NO
        )
        self.assertTrue(antenatal_enrollment.eligible_for_postnatal)

    def test_breastfeed_for_a_year(self):
        """Test for a negative mother who agrees to breastfeed for a year."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            verbal_hiv_status=NEG,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            breastfeed_for_a_year=YES
        )
        self.assertTrue(antenatal_enrollment.eligible_for_postnatal)

    def test_no_breastfeed_for_a_year(self):
        """Test for a negative mother who does not agree to breastfeed for a year."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            verbal_hiv_status=NEG,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            breastfeed_for_a_year=NO
        )
        self.assertFalse(antenatal_enrollment.eligible_for_postnatal)

    def test_instudy_for_a_year(self):
        """Test for a negative mother who does agrees to stay in study a year."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            verbal_hiv_status=NEG,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            instudy_for_a_year=YES
        )
        self.assertTrue(antenatal_enrollment.eligible_for_postnatal)

    def test_not_instudy_for_a_year(self):
        """Test for a negative mother who does not agree to stay in study for a year."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            verbal_hiv_status=NEG,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            instudy_for_a_year=NO
        )
        self.assertFalse(antenatal_enrollment.eligible_for_postnatal)

    def test_positive_with_evidence(self):
        """Test for a negative mother with evidence."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            verbal_hiv_status=NEG,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
        )
        self.assertTrue(antenatal_enrollment.eligible_for_postnatal)

    def test_positive_with_no_evidence_and_rapid_test_done(self):
        """Test for a negative mother with no evidence and test not done."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            verbal_hiv_status=POS,
            evidence_hiv_status=NO,
            registered_subject=self.registered_subject,
            process_rapid_test=NO,
        )
        self.assertFalse(antenatal_enrollment.eligible_for_postnatal)

    def test_positive_with_no_evidence_and_gestation_37(self):
        """Test for a positive mother with no evidence and gestation 37 weeks."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            verbal_hiv_status=POS,
            evidence_hiv_status=NO,
            registered_subject=self.registered_subject,
            process_rapid_test=NO,
            weeks_of_gestation=37,
        )
        self.assertFalse(antenatal_enrollment.eligible_for_postnatal)

    def test_fail_fill_antenatal_if_postnatal_filled(self):
        """Test that antenatal fails if filled after postnatal is completed."""
        PostnatalEnrollmentFactory(registered_subject=self.registered_subject)
        AntenatalEnrollmentFactory(registered_subject=self.registered_subject)
        self.assertRaises(forms.ValidationError)

    def test_cannot_change_rapid_test_date(self):
        antenatal = AntenatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            verbal_hiv_status=NEG,
            evidence_hiv_status=NO,
            valid_regimen=NOT_APPLICABLE,
            valid_regimen_duration=NOT_APPLICABLE,
            process_rapid_test=YES,
            date_of_rapid_test=timezone.now().date() - timezone.timedelta(days=1),
            rapid_test_result=POS)
        self.assertTrue(AntenatalEnrollment.objects.count(), 1)
        antenatal.date_of_rapid_test = timezone.now().date()
        antenatal.save()
        self.assertRaises(forms.ValidationError)

    def test_mother_tested_at_32weeks_with_evidence(self):
        """Test for a mother tested at 32weeks with evidence"""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            week32_test=YES,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            weeks_of_gestation=37
        )
        self.assertTrue(antenatal_enrollment.eligible_for_postnatal)

    def test_mother_tested_at_32weeks_without_evidence(self):
        """Test for a mother tested at 32weeks without evidence"""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            week32_test=YES,
            evidence_hiv_status=NO,
            registered_subject=self.registered_subject,
            weeks_of_gestation=37
        )
        self.assertFalse(antenatal_enrollment.eligible_for_postnatal)

    def test_no_week32test_no_rapid_test(self):
        """Test for a mother who did not test at week 32 and does not do rapid test"""
        antenatal_enrollment = AntenatalEnrollmentFactory(
            week32_test=NO,
            week32_result=None,
            evidence_hiv_status=NO,
            process_rapid_test=NO,
            registered_subject=self.registered_subject,
            weeks_of_gestation=37
        )
        self.assertFalse(antenatal_enrollment.eligible_for_postnatal)

    def test_no_week32test_does_rapid_test(self):
        """Test for a mother who did not test at week 32 and does a rapid test"""
        antenatal_enrollment = AntenatalEnrollmentFactory(
            week32_test=NO,
            week32_result='',
            process_rapid_test=YES,
            registered_subject=self.registered_subject,
            weeks_of_gestation=37
        )
        self.assertTrue(antenatal_enrollment.eligible_for_postnatal)
