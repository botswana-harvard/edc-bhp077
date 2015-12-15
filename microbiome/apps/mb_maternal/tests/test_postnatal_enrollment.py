from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc_constants.choices import YES, NO, POS, NEG, NOT_APPLICABLE

from ..maternal_choices import STILL_BIRTH, LIVE
from ..visit_schedule import PostnatalEnrollmentVisitSchedule
from microbiome.apps.mb.app_configuration.classes import MicrobiomeConfiguration
from microbiome.apps.mb_lab.lab_profiles import MaternalProfile
from microbiome.apps.mb_maternal.models import AntenatalEnrollment
from microbiome.apps.mb_maternal.tests.factories import MaternalConsentFactory
from microbiome.apps.mb_maternal.tests.factories import MaternalEligibilityFactory
from microbiome.apps.mb_maternal.tests.factories import PostnatalEnrollmentFactory, AntenatalEnrollmentFactory
from edc_constants.constants import UNKNOWN, DWTA, NEVER
from microbiome.apps.mb_maternal.models.postnatal_enrollment import PostnatalEnrollment
from django.utils import timezone
from microbiome.apps.mb_maternal.models.enrollment_helper import EnrollmentError


class TestPostnatalEnrollment(TestCase):
    """Test eligibility of a mother for postnatal enrollment."""

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        PostnatalEnrollmentVisitSchedule().build()
        site_rule_groups.autodiscover()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject

    def test_breatfeed_yes(self):
        """Test for when breast feeding for a year is yes."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            will_breastfeed=YES
        )
        self.assertTrue(postnatal_enrollment.is_eligible)

    def test_breatfeed_no(self):
        """Test for when breast feeding for a year is no."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            will_breastfeed=NO)
        self.assertFalse(postnatal_enrollment.is_eligible)

    def test_on_tb_tx(self):
        """Test for when on tb treatment."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            on_tb_tx=YES)
        self.assertFalse(postnatal_enrollment.is_eligible)

    def test_not_on_tb_tx(self):
        """Test for when not on tb treatment."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            on_tb_tx=NO)
        self.assertTrue(postnatal_enrollment.is_eligible)

    def test_is_diabetic(self):
        """Test for a subject who is diabetic."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            is_diabetic=YES)
        self.assertFalse(postnatal_enrollment.is_eligible)

    def test_is_not_diabetic(self):
        """Test for a subject who is not diabetic."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            is_diabetic=NO)
        self.assertTrue(postnatal_enrollment.is_eligible)

    def test_will_remain_onstudy(self):
        """Test for a subject who is in the study for a year."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            will_remain_onstudy=YES)
        self.assertTrue(postnatal_enrollment.is_eligible)

    def test_not_will_remain_onstudy(self):
        """Test for a subject who is not in the study for a year."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            will_remain_onstudy=NO)
        self.assertFalse(postnatal_enrollment.is_eligible)

    def test_postpartum_days_more_than_3_days(self):
        """Test for a subject whose postpartum days is more than 3 days."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            postpartum_days=4)
        self.assertFalse(postnatal_enrollment.is_eligible)

    def test_postpartum_days_less_than_3_days(self):
        """Test for a subject whose postpartum days is less than 3 days."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            postpartum_days=2)
        self.assertTrue(postnatal_enrollment.is_eligible)

    def test_postpartum_days_equal_3_days(self):
        """Test for a subject whose postpartum days is equals 3 days."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            postpartum_days=3)
        self.assertTrue(postnatal_enrollment.is_eligible)

    def test_vaginal_delivery_vaginal(self):
        """Test for a subject whose delivery type is vaginal."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            vaginal_delivery=YES)
        self.assertTrue(postnatal_enrollment.is_eligible)

    def test_vaginal_delivery_not_vaginal(self):
        """Test for a subject whose delivery type is vaginal."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            vaginal_delivery=NO)
        self.assertFalse(postnatal_enrollment.is_eligible)

    def test_still_birth(self):
        """Test for a subject who had a still birth."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            delivery_status=STILL_BIRTH)
        self.assertFalse(postnatal_enrollment.is_eligible)

    def test_live_birth(self):
        """Test for a subject who had a live birth."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            delivery_status=LIVE)
        self.assertTrue(postnatal_enrollment.is_eligible)

    def test_gestation_wks_delivered_below_37(self):
        """Test for a subject whose gestation before birth is below 37."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            gestation_wks_delivered=36)
        self.assertFalse(postnatal_enrollment.is_eligible)

    def test_gestation_wks_delivered_equal_37(self):
        """Test for a subject whose gestation before birth is equals to 37."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            gestation_wks_delivered=37)
        self.assertTrue(postnatal_enrollment.is_eligible)

    def test_gestation_wks_delivered_above_37(self):
        """Test for a subject whose gestation before birth is above 37."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            gestation_wks_delivered=38)
        self.assertTrue(postnatal_enrollment.is_eligible)

    def test_pos_has_evidence_valid_regimen_valid_regimen_duration(self):
        """Test for a subject who is positive, has evidence, valid regimen, valid regimen duration."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            valid_regimen=YES,
            valid_regimen_duration=YES)
        self.assertTrue(postnatal_enrollment.is_eligible)

    def test_pos_has_evidence_no_valid_regimen(self):
        """Test for a subject who is positive, has evidence, no valid regimen."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            valid_regimen=NO)
        self.assertFalse(postnatal_enrollment.is_eligible)

    def test_pos_has_evidence_valid_regimen_unvalid_regimen_duration(self):
        """Test for a subject who is positive, has evidence, valid regimen, unvalid regimen duration."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            valid_regimen=YES,
            valid_regimen_duration=NO)
        self.assertFalse(postnatal_enrollment.is_eligible)

    def test_negative_with_evidence(self):
        """Test for a subject whose verbal hiv status is negative and has evidence."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        self.assertTrue(postnatal_enrollment.is_eligible)

    def test_negative_with_no_evidence(self):
        """Test for a subject whose verbal hiv status is negative and has no evidence."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=NO,
            valid_regimen=NOT_APPLICABLE,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        self.assertTrue(postnatal_enrollment.is_eligible)

    def test_current_hiv_status_neg_with_no_evidence(self):
        """Test for a subject whose verbal hiv status is NEG and has no evidence, rapid test result POS."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=NO,
            valid_regimen=NOT_APPLICABLE,
            rapid_test_done=YES,
            rapid_test_result=POS)
        self.assertFalse(postnatal_enrollment.is_eligible)

    def test_current_hiv_status_never_tested_for_HIV_1(self):
        """Test for a subject whose current_hiv_status is Never but tests NEG on rapid."""
        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEVER,
            evidence_hiv_status=NOT_APPLICABLE,
            valid_regimen=NOT_APPLICABLE,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        self.assertTrue(postnatal_enrollment.is_eligible)

    def test_current_hiv_status_never_tested_for_HIV_2(self):
        """Test for a subject whose current_hiv_status is Never but tests POS on rapid."""
        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEVER,
            evidence_hiv_status=NOT_APPLICABLE,
            rapid_test_done=YES,
            rapid_test_result=POS,
            valid_regimen=NOT_APPLICABLE)
        self.assertFalse(postnatal_enrollment.is_eligible)

    def test_current_hiv_status_unknown_rapid_test_result_neg(self):
        """Test for a subject whose verbal hiv status is unknown and rapid test result NEG."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=UNKNOWN,
            evidence_hiv_status=NOT_APPLICABLE,
            valid_regimen=NOT_APPLICABLE,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        self.assertTrue(postnatal_enrollment.is_eligible)

    def test_current_hiv_status_unknown_rapid_test_result_pos(self):
        """Test for a subject whose verbal hiv status is unknown and rapid test result POS."""
        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=UNKNOWN,
            evidence_hiv_status=NOT_APPLICABLE,
            valid_regimen=NOT_APPLICABLE,
            rapid_test_done=YES,
            rapid_test_result=POS)
        self.assertFalse(postnatal_enrollment.is_eligible)

    def test_current_hiv_status_refused_to_answer_rapid_test_result_pos(self):
        """Test for a subject whose verbal hiv status is refused to answer and rapid test result POS."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=DWTA,
            evidence_hiv_status=NOT_APPLICABLE,
            valid_regimen=NOT_APPLICABLE,
            rapid_test_done=YES,
            rapid_test_result=POS)
        self.assertFalse(postnatal_enrollment.is_eligible)

    def test_current_hiv_status_refused_to_answer_rapid_test_result_neg(self):
        """Test for a subject whose verbal hiv status is refused to answer and rapid test result NEG."""

        postnatal_enrollment = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=DWTA,
            evidence_hiv_status=NOT_APPLICABLE,
            valid_regimen=NOT_APPLICABLE,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        self.assertTrue(postnatal_enrollment.is_eligible)

    def test_pos_with_evidence(self):
        """Test that pos subject with evidence has unchanging status on postnatal enrollment"""
        antenatal = AntenatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE)
        self.assertEqual(AntenatalEnrollment.objects.count(), 1)
        postnatal = PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject)
        self.assertEqual(antenatal.current_hiv_status, postnatal.current_hiv_status)
        self.assertEqual(antenatal.evidence_hiv_status, postnatal.evidence_hiv_status)

    def test_updates_postnatal_with_antenatal(self):
        """Test that common fields not provided at postnatal are fetched from antenatal."""
        AntenatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        antenatal_enrollment = AntenatalEnrollment.objects.get(
            registered_subject=self.registered_subject)
        self.assertEqual(antenatal_enrollment.current_hiv_status, NEG)
        self.assertEqual(antenatal_enrollment.evidence_hiv_status, YES)
        self.assertTrue(antenatal_enrollment.is_eligible)
        PostnatalEnrollment.objects.create(
            report_datetime=timezone.now(),
            registered_subject=self.registered_subject,
            delivery_status=LIVE,
            gestation_wks_delivered=38,
            is_diabetic=NO,
            live_infants=1,
            on_tb_tx=NO,
            postpartum_days=2,
            vaginal_delivery=YES,
            will_breastfeed=YES,
            will_remain_onstudy=YES)
        postnatal_enrollment = PostnatalEnrollment.objects.get(
            registered_subject=self.registered_subject)
        self.assertTrue(postnatal_enrollment.is_eligible)
        self.assertEqual(
            antenatal_enrollment.current_hiv_status,
            postnatal_enrollment.current_hiv_status)
        self.assertEqual(
            antenatal_enrollment.evidence_hiv_status,
            postnatal_enrollment.evidence_hiv_status)

    def test_only_updates_postnatal_with_antenatal_if_not_provided(self):
        """Assert common value provided in postnatal is NOT overwritten by antenatal.

        Note 'rapid_test_result' is changed on postnatal."""
        AntenatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)
        antenatal_enrollment = AntenatalEnrollment.objects.get(
            registered_subject=self.registered_subject)
        self.assertEqual(antenatal_enrollment.current_hiv_status, NEG)
        self.assertEqual(antenatal_enrollment.evidence_hiv_status, YES)
        self.assertTrue(antenatal_enrollment.is_eligible)
        PostnatalEnrollment.objects.create(
            rapid_test_done=YES,
            rapid_test_result=POS,
            report_datetime=timezone.now(),
            registered_subject=self.registered_subject,
            delivery_status=LIVE,
            gestation_wks_delivered=38,
            is_diabetic=NO,
            live_infants=1,
            on_tb_tx=NO,
            on_hypertension_tx=NO,
            postpartum_days=2,
            vaginal_delivery=YES,
            will_breastfeed=YES,
            will_remain_onstudy=YES)
        postnatal_enrollment = PostnatalEnrollment.objects.get(
            registered_subject=self.registered_subject)
        self.assertNotEqual(
            antenatal_enrollment.rapid_test_result,
            postnatal_enrollment.rapid_test_result)
        self.assertFalse(postnatal_enrollment.is_eligible)

    def test_does_not_update_from_ineligible_antenatal(self):
        """Asserts that common fields are not fetched from AntenatalEnrollment if
        AntenatalEnrollment.is_eligible=False."""
        AntenatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=POS)
        antenatal_enrollment = AntenatalEnrollment.objects.get(
            registered_subject=self.registered_subject)
        self.assertFalse(antenatal_enrollment.is_eligible)
        with self.assertRaises(EnrollmentError) as cm:
            PostnatalEnrollment.objects.create(
                report_datetime=timezone.now(),
                registered_subject=self.registered_subject,
                delivery_status=LIVE,
                gestation_wks_delivered=38,
                is_diabetic=NO,
                live_infants=1,
                on_tb_tx=NO,
                postpartum_days=2,
                vaginal_delivery=YES,
                will_breastfeed=YES,
                will_remain_onstudy=YES)
        self.assertEqual(
            str(cm.exception),
            ('Unable to determine maternal hiv status at enrollment. Got current_hiv_status=, '
             'evidence_hiv_status=None, rapid_test_done=None, rapid_test_result=None'))
