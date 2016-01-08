from datetime import timedelta
from django.utils import timezone

from edc_appointment.models import Appointment
from edc_appointment.tests.factories.appointment_factory import AppointmentFactory
from edc_constants.constants import (
    POS, YES, NEG, NOT_APPLICABLE, FAILED_ELIGIBILITY, UNKEYED, SCHEDULED, NOT_REQUIRED)
from edc_meta_data.models import CrfMetaData

from .factories import (
    MaternalEligibilityFactory, MaternalConsentFactory, AntenatalEnrollmentFactory,
    PostnatalEnrollmentFactory)
from microbiome.apps.mb_maternal.tests.base_maternal_test_case import BaseMaternalTestCase
from microbiome.apps.mb_maternal.models.enrollment_loss import (
    AntenatalEnrollmentLoss, PostnatalEnrollmentLoss)
from microbiome.apps.mb_maternal.models import MaternalVisit


class TestEnrollmentLoss(BaseMaternalTestCase):
    """Test failed enrollment creates enrollment loss form"""

    def setUp(self):
        super(TestEnrollmentLoss, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject
        self.antenatal_enrollment = AntenatalEnrollmentFactory(
            gestation_wks=35,
            week32_test=YES,
            week32_result=NEG,
            week32_test_date=timezone.now().date() - timedelta(weeks=3),
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            valid_regimen=NOT_APPLICABLE,
            valid_regimen_duration=NOT_APPLICABLE,
            rapid_test_done=NOT_APPLICABLE,
            registered_subject=self.registered_subject)

    def test_failed_enrollment_makes_loss_entry(self):
        """Test mother enrolled with less than 36 weeks gestation makes an enrollment loss entry"""
        self.assertFalse(self.antenatal_enrollment.is_eligible)
        self.assertEqual(AntenatalEnrollmentLoss.objects.all().count(), 1)

    def test_failed_enrollment_creates_failed_visit(self):
        """Test if enrollment failed that proceeding to visit automatically sets visit reason
        to failed_eligibility"""
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        self.assertTrue(MaternalVisit.objects.get(
            appointment=appointment, reason=FAILED_ELIGIBILITY))

    def test_failed_enrollment_allows_off_study_form_only(self):
        """Test if enrollment failed and appointment status is failed_eligibility that only
        the off study form is required"""
        appointment = Appointment.objects.get(
            registered_subject=self.registered_subject,
            visit_definition__code='1000M')
        MaternalVisit.objects.get(appointment=appointment, reason=FAILED_ELIGIBILITY)
        self.assertEqual(
            CrfMetaData.objects.filter(
                appointment=appointment,
                entry_status=UNKEYED,
                crf_entry__app_label='mb_maternal',
                crf_entry__model_name='maternaloffstudy').count(), 1)

    def test_changing_ineligble_to_eligible(self):
        """Test ineligible mother made eligible now deletes enrollment loss entry"""
        self.antenatal_enrollment.gestation_wks = 37
        self.antenatal_enrollment.save()
        self.assertTrue(self.antenatal_enrollment.is_eligible)
        self.assertEqual(AntenatalEnrollmentLoss.objects.all().count(), 0)

    def test_eligible_mother_has_scheduled_visit(self):
        """Test that since mother is made eligible, that 1000M visit reason is flipped to
        scheduled"""
        self.antenatal_enrollment.gestation_wks = 37
        self.antenatal_enrollment.save()
        appointment = Appointment.objects.get(
            registered_subject=self.antenatal_enrollment.registered_subject,
            visit_definition__code='1000M')
        self.assertTrue(MaternalVisit.objects.get(
            appointment=appointment, reason=SCHEDULED))

    def test_eligible_mother_scheduled_visit_has_no_off_study(self):
        """Test that the mothers now scheduled visit now has off study set to not_required"""
        self.antenatal_enrollment.gestation_wks = 37
        self.antenatal_enrollment.save()
        appointment = Appointment.objects.get(
            registered_subject=self.antenatal_enrollment.registered_subject,
            visit_definition__code='1000M')
        MaternalVisit.objects.get(appointment=appointment, reason=SCHEDULED)
        self.assertEqual(
            CrfMetaData.objects.filter(
                appointment=appointment,
                entry_status=NOT_REQUIRED,
                crf_entry__app_label='mb_maternal',
                crf_entry__model_name='maternaloffstudy').count(), 1)

    def test_eligible_mother_scheduled_visit_has_correct_forms(self):
        """Test that the mothers all required forms for a scheduled visit"""
        self.antenatal_enrollment.gestation_wks = 37
        self.antenatal_enrollment.save()
        appointment = Appointment.objects.get(
            registered_subject=self.antenatal_enrollment.registered_subject,
            visit_definition__code='1000M')
        MaternalVisit.objects.get(appointment=appointment, reason=SCHEDULED)
        self.assertEqual(
            CrfMetaData.objects.filter(
                appointment=appointment,
                entry_status=UNKEYED,
                crf_entry__app_label='mb_maternal',
                crf_entry__model_name__in=[
                    'maternallocator', 'maternaldemographics', 'maternalmedicalhistory',
                    'maternalobstericalhistory']).count(), 4)

    def test_failed_postnatal_enrollment_for_pos(self):
        """Test a failed postnatal enrollment created enrollment loss"""
        maternal_eligibility = MaternalEligibilityFactory()
        maternal_consent = MaternalConsentFactory(
            registered_subject=maternal_eligibility.registered_subject)
        registered_subject = maternal_consent.registered_subject
        postnatal_enrollment = PostnatalEnrollmentFactory(
            gestation_wks_delivered=35,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            registered_subject=registered_subject)
        self.assertFalse(postnatal_enrollment.is_eligible)
        self.assertEqual(PostnatalEnrollmentLoss.objects.all().count(), 1)

    def test_failed_postnatal_enrollment_for_pos_creates_failed_visit(self):
        """Test a failed postnatal enrollment for pos mother creates a failed_eligibility visit"""
        maternal_eligibility = MaternalEligibilityFactory()
        maternal_consent = MaternalConsentFactory(
            registered_subject=maternal_eligibility.registered_subject)
        registered_subject = maternal_consent.registered_subject
        postnatal_enrollment = PostnatalEnrollmentFactory(
            gestation_wks_delivered=35,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            registered_subject=registered_subject)
        self.assertFalse(postnatal_enrollment.is_eligible)
        appointment = Appointment.objects.get(
            registered_subject=postnatal_enrollment.registered_subject,
            visit_definition__code='1000M')
        self.assertTrue(MaternalVisit.objects.get(
            appointment=appointment, reason=FAILED_ELIGIBILITY))
