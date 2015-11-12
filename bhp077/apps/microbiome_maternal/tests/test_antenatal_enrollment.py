from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc_constants.choices import POS, YES, NO, NEG

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_maternal.tests.factories import AntenatalEnrollmentFactory, MaternalEligibilityFactory
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

    def test_weeks_of_gestation_below_32(self):
        """Test for a positive mother on a valid regimen but weeks of gestation below 32."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            verbal_hiv_status=POS,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            weeks_of_gestation=30
        )
        self.assertFalse(antenatal_enrollment.eligible_for_postnatal)

    def test_weeks_of_gestation_above_32_and_no_regime(self):
        """Test for a positive mother not on a valid regimen but weeks of gestation above 32."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            verbal_hiv_status=POS,
            evidence_hiv_status=YES,
            valid_regimen=NO,
            registered_subject=self.registered_subject,
            weeks_of_gestation=34
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
        """Test for a negative mother who does not agree to breastfeed for a year."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            verbal_hiv_status=NEG,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            instudy_for_a_year=YES
        )
        self.assertTrue(antenatal_enrollment.eligible_for_postnatal)

    def test_not_instudy_for_a_year(self):
        """Test for a negative mother who does not agree to breastfeed for a year."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            verbal_hiv_status=NEG,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
            instudy_for_a_year=NO
        )
        self.assertTrue(antenatal_enrollment.eligible_for_postnatal)

    def test_posotive_with_evidence(self):
        """Test for a negative mother with evidence."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            verbal_hiv_status=NEG,
            evidence_hiv_status=YES,
            registered_subject=self.registered_subject,
        )
        self.assertTrue(antenatal_enrollment.eligible_for_postnatal)

    def test_posotive_with_no_evidence_and_rapid_test_done(self):
        """Test for a negative mother with no evidence and test not done."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            verbal_hiv_status=POS,
            evidence_hiv_status=NO,
            registered_subject=self.registered_subject,
            process_rapid_test=NO,
        )
        self.assertFalse(antenatal_enrollment.eligible_for_postnatal)

    def test_posotive_with_no_evidence_and_gestation_33(self):
        """Test for a positive mother with no evidence and gestation 33 weeks."""

        antenatal_enrollment = AntenatalEnrollmentFactory(
            verbal_hiv_status=POS,
            evidence_hiv_status=NO,
            registered_subject=self.registered_subject,
            process_rapid_test=NO,
            weeks_of_gestation=33,
        )
        self.assertFalse(antenatal_enrollment.eligible_for_postnatal)
