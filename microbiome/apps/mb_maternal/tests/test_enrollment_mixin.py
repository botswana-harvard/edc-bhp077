from datetime import date
from django.utils import timezone
from django.db import models

from edc_constants.constants import POS, YES, NO, NEG, NOT_APPLICABLE, NEVER
from edc_registration.models import RegisteredSubject

from microbiome.apps.mb_maternal.tests.factories import (
    MaternalEligibilityFactory, MaternalConsentFactory, SpecimenConsentFactory)
from microbiome.apps.mb_maternal.forms import BaseEnrollmentForm
from microbiome.apps.mb_maternal.models.enrollment_mixin import EnrollmentMixin
from microbiome.apps.mb_maternal.models.antenatal_enrollment import AntenatalEnrollment
from dateutil.relativedelta import relativedelta
from microbiome.apps.mb_maternal.models.enrollment_helper import EnrollmentHelper, EnrollmentError

from .base_test_case import BaseTestCase


class EnrollmentTestModel(EnrollmentMixin):

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    report_datetime = models.DateTimeField(
        default=timezone.now())

    def save_common_fields_to_postnatal_enrollment(self):
        pass

    def save(self, *args, **kwargs):
        self.is_eligible = True
        super(EnrollmentTestModel, self).save(*args, **kwargs)

    class Meta:
        app_label = 'mb_maternal'


class BaseEnrollTestForm(BaseEnrollmentForm):

    class Meta:
        model = EnrollmentTestModel
        fields = '__all__'


class TestEnrollmentMixin(BaseTestCase):
    """Test eligibility of a mother for antenatal enrollment."""

    def setUp(self):
        super(TestEnrollmentMixin, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject
        self.specimen_consent = SpecimenConsentFactory(registered_subject=self.registered_subject)
        self.data = {
            'registered_subject': self.registered_subject.id,
            'report_datetime': timezone.now(),
            'is_diabetic': NO,
            'on_tb_tx': NO,
            'will_breastfeed': NO,
            'will_remain_onstudy': NO,
            'week32_test': NO,
            'week32_result': '',
            'current_hiv_status': POS,
            'evidence_hiv_status': NO,
            'valid_regimen': NO,
            'valid_regimen_duration': NOT_APPLICABLE,
            'rapid_test_done': NO,
            'rapid_test_date': '',
            'rapid_test_result': '',
        }

    def test_process_rapid_yes_date_req(self):
        """If rapid test was processed, test date was processed is required"""
        self.data['rapid_test_done'] = YES
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn('You indicated that a rapid test was processed. Please provide the date.',
                      form.errors.get('__all__'))

    def test_process_rapid_no_date_req(self):
        """If rapid test was NOT processed, test date was processed is  NOT required"""
        self.data['rapid_test_done'] = NO
        self.data['rapid_test_date'] = date.today()
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn('You indicated that a rapid test was NOT processed, yet rapid test date was provided. '
                      'Please correct.', form.errors.get('__all__'))

    def test_process_rapid_na_date_req(self):
        """If rapid test was NOT processed, test date was processed is  NOT required"""
        self.data['rapid_test_done'] = NOT_APPLICABLE
        self.data['rapid_test_date'] = date.today()
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn('You indicated that a rapid test was NOT processed, yet rapid test date was provided. '
                      'Please correct.', form.errors.get('__all__'))

    def test_process_rapid_yes_result_req(self):
        """If rapid test was processed, test result was processed is required"""
        self.data['rapid_test_done'] = YES
        self.data['rapid_test_date'] = date.today()
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn('You indicated that a rapid test was processed. Please provide a result.',
                      form.errors.get('__all__'))

    def test_process_rapid_no_result_not_req(self):
        """If rapid test was NOT processed, test result was processed is NOT required"""
        self.data['rapid_test_done'] = NO
        self.data['rapid_test_result'] = POS
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn('You indicated that a rapid test was NOT processed, yet rapid test result was provided. '
                      'Please correct.', form.errors.get('__all__'))

    def test_process_rapid_na_result_not_req(self):
        """If rapid test was NOT processed, test result was processed is NOT required"""
        self.data['rapid_test_done'] = NOT_APPLICABLE
        self.data['rapid_test_result'] = NEG
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn('You indicated that a rapid test was NOT processed, yet rapid test result was provided. '
                      'Please correct.', form.errors.get('__all__'))

    def test_regimen_duration_na(self):
        self.data['valid_regimen'] = YES
        self.data['valid_regimen_duration'] = NOT_APPLICABLE
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn('You have indicated that the participant is on ARV. Regimen validity period'
                      ' CANNOT be \'Not Applicable\'. Please correct.', form.errors.get('__all__'))

    def test_regimen_duration_yes(self):
        self.data['valid_regimen'] = NO
        self.data['valid_regimen_duration'] = YES
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn('You have indicated that there are no records of Participant taking ARVs. '
                      'Regimen validity period should be \'Not Applicable\'. '
                      'Please correct.', form.errors.get('__all__'))

    def test_regimen_duration_no(self):
        self.data['valid_regimen'] = NO
        self.data['valid_regimen_duration'] = NO
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn('You have indicated that there are no records of Participant taking ARVs. '
                      'Regimen validity period should be \'Not Applicable\'. '
                      'Please correct.', form.errors.get('__all__'))

    def test_hiv_evidence_pos(self):
        self.data['evidence_hiv_status'] = NOT_APPLICABLE
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn('You have indicated that the participant is Positive, Evidence of HIV '
                      'result CANNOT be \'Not Applicable\'. Please correct.', form.errors.get('__all__'))

    def test_hiv_evidence_pos_reg_na(self):
        self.data['valid_regimen'] = NOT_APPLICABLE
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn('You have indicated that the participant is Positive, \'do records show that'
                      ' participant takes ARVs\' cannot be \'Not Applicable\'.', form.errors.get('__all__'))

    def test_hiv_evidence_neg(self):
        self.data['current_hiv_status'] = NEG
        self.data['evidence_hiv_status'] = NOT_APPLICABLE
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn('You have indicated that the participant is Negative, Evidence of HIV '
                      'result CANNOT be \'Not Applicable\'. Please correct.', form.errors.get('__all__'))

    def test_sample_filled_before_enrollment(self):
        self.specimen_consent.delete()
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn('Please ensure to save the Specimen Consent before completing Enrollment',
                      form.errors.get('__all__'))

    def test_pos_with_evidence_and_do_rapid_test(self):
        self.data['evidence_hiv_status'] = YES
        self.data['rapid_test_done'] = YES
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn('There is no need for a rapid test. Subject is positive and has evidence.',
                      form.errors.get('__all__'))

    def test_participant_never_tested(self):
        self.data['current_hiv_status'] = NEVER
        self.data['evidence_hiv_status'] = NOT_APPLICABLE
        self.data['valid_regimen'] = NOT_APPLICABLE
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn('Participant current HIV status is {}. You must conduct HIV rapid testing '
                      'today to continue with the eligibility screen'.format(
                          self.data['current_hiv_status']), form.errors.get('__all__'))

    def test_results_comparison(self):
        self.data['week32_test'] = YES
        self.data['week32_result'] = NEG
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn(
            'The current hiv status and result at 32weeks should be the same!',
            form.errors.get('__all__'))

    def test_tested_at_32weeks_no_result(self):
        self.data['week32_test'] = YES
        self.data['week32_result'] = None
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn('Please provide test result at week 32.', form.errors.get('__all__'))

    def test_not_tested_at_32weeks_results_given(self):
        self.data['week32_result'] = POS
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn(
            'You mentioned testing was not done at 32weeks yet provided a '
            'test result.', form.errors.get('__all__'))

    def test_date_at_32wks(self):
        """Asserts the test date is correctly calculated to be on or after 32 wks."""
        obj = AntenatalEnrollment(
            week32_test_date=date.today() - relativedelta(weeks=7),
            gestation_wks=38,
            report_datetime=timezone.now())
        enrollment_helper = EnrollmentHelper(obj)
        self.assertFalse(enrollment_helper.test_date_is_on_or_after_32wks())

        obj = AntenatalEnrollment(
            week32_test_date=date.today() - relativedelta(weeks=6),
            gestation_wks=38,
            report_datetime=timezone.now())
        enrollment_helper = EnrollmentHelper(obj)
        self.assertTrue(enrollment_helper.test_date_is_on_or_after_32wks())

        obj = AntenatalEnrollment(
            week32_test_date=date.today() - relativedelta(weeks=5),
            gestation_wks=38,
            report_datetime=timezone.now())
        enrollment_helper = EnrollmentHelper(obj)
        self.assertTrue(enrollment_helper.test_date_is_on_or_after_32wks())

        obj = AntenatalEnrollment(
            week32_test_date=date.today(),
            gestation_wks=38,
            report_datetime=timezone.now())
        enrollment_helper = EnrollmentHelper(obj)
        self.assertTrue(enrollment_helper.test_date_is_on_or_after_32wks())

    def test_neg_rapid_not_required(self):
        """Assert rapid not required if last test was within 32 weeks."""
        obj = AntenatalEnrollment(
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            week32_test=YES,
            week32_test_date=date(2015, 11, 13),
            week32_result=NEG,
            rapid_test_done=NOT_APPLICABLE,
            report_datetime=timezone.datetime(2015, 12, 11, 0, 0, 0),
            gestation_wks=36,
            is_diabetic=NO,
            on_tb_tx=NO,
            on_hypertension_tx=NO,
            will_breastfeed=YES,
            will_remain_onstudy=YES)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertTrue(enrollment_helper.is_eligible)

    def test_neg_rapid_required_raises_on_invalid_week32_date(self):
        obj = AntenatalEnrollment(
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            week32_test=YES,
            week32_test_date=date(2015, 11, 1),
            week32_result=NEG,
            rapid_test_done=NOT_APPLICABLE,
            report_datetime=timezone.datetime(2015, 12, 11, 0, 0, 0),
            gestation_wks=36,
            is_diabetic=NO,
            on_tb_tx=NO,
            on_hypertension_tx=NO,
            will_breastfeed=YES,
            will_remain_onstudy=YES)
        self.assertRaises(EnrollmentError, EnrollmentHelper, obj)

    def test_neg_rapid_required(self):
        obj = AntenatalEnrollment(
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            week32_test=NO,
            rapid_test_done=NOT_APPLICABLE,
            report_datetime=timezone.datetime(2015, 12, 11, 0, 0, 0),
            gestation_wks=36,
            is_diabetic=NO,
            on_tb_tx=NO,
            on_hypertension_tx=NO,
            will_breastfeed=YES,
            will_remain_onstudy=YES)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertFalse(enrollment_helper.is_eligible)

    def test_neg_rapid_required2(self):
        obj = AntenatalEnrollment(
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            week32_test=YES,
            week32_test_date=date(2015, 11, 13),
            week32_result=NEG,
            rapid_test_done=YES,
            rapid_test_date=date(2015, 12, 11),
            rapid_test_result=NEG,
            report_datetime=timezone.datetime(2015, 12, 11, 0, 0, 0),
            gestation_wks=36,
            is_diabetic=NO,
            on_tb_tx=NO,
            on_hypertension_tx=NO,
            will_breastfeed=YES,
            will_remain_onstudy=YES)
        enrollment_helper = EnrollmentHelper(obj)
        self.assertTrue(enrollment_helper.is_eligible)

    def test_neg_rapid_required_invalid_rapid_test_date(self):
        obj = AntenatalEnrollment(
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            week32_test=YES,
            week32_test_date=date(2015, 11, 13),
            week32_result=NEG,
            rapid_test_done=YES,
            rapid_test_date=date(2015, 11, 12),
            rapid_test_result=NEG,
            report_datetime=timezone.datetime(2015, 12, 11, 0, 0, 0),
            gestation_wks=36,
            is_diabetic=NO,
            on_tb_tx=NO,
            on_hypertension_tx=NO,
            will_breastfeed=YES,
            will_remain_onstudy=YES)
        self.assertRaises(EnrollmentError, EnrollmentHelper, obj)
