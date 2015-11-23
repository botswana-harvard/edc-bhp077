from django.test import TestCase
from django.utils import timezone
from django import forms

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc_constants.choices import POS, YES, NO, NEG, NOT_APPLICABLE

from bhp077.apps.microbiome.app_configuration.classes import MicrobiomeConfiguration
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from bhp077.apps.microbiome_maternal.tests.factories import (MaternalEligibilityFactory,
                                                             MaternalConsentFactory,
                                                             SampleConsentFactory)
from bhp077.apps.microbiome_maternal.models import BaseEnrollment
from bhp077.apps.microbiome_maternal.forms import BaseEnrollmentForm


class BaseEnrollTestModel(BaseEnrollment):
    class Meta:
        app_label = 'microbiome_maternal'


class BaseEnrollTestForm(BaseEnrollmentForm):

    class Meta:
        model = BaseEnrollTestModel
        fields = '__all__'


class TestBaseEnroll(TestCase):
    """Test eligibility of a mother for antenatal enrollment."""

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        site_rule_groups.autodiscover()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject
        self.data = {
            'registered_subject': self.registered_subject.id,
            'report_datetime': timezone.datetime.today(),
            'is_diabetic': NO,
            'on_tb_treatment': NO,
            'breastfeed_for_a_year': NO,
            'instudy_for_a_year': NO,
            'verbal_hiv_status': POS,
            'evidence_hiv_status': NO,
            'valid_regimen': NO,
            'valid_regimen_duration': NOT_APPLICABLE,
            'process_rapid_test': NO,
            'date_of_rapid_test': '',
            'rapid_test_result': '',
        }

    def test_process_rapid_yes_date_req(self):
        """If rapid test was processed, test date was processed is required"""
        self.data['process_rapid_test'] = YES
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn(u'You indicated that a rapid test was processed. Please provide the date.',
                      form.errors.get('__all__'))

    def test_process_rapid_no_date_req(self):
        """If rapid test was NOT processed, test date was processed is  NOT required"""
        self.data['process_rapid_test'] = NO
        self.data['date_of_rapid_test'] = timezone.now().date()
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn(u'You indicated that a rapid test was NOT processed, yet rapid test date was provided. '
                      'Please correct.', form.errors.get('__all__'))

    def test_process_rapid_na_date_req(self):
        """If rapid test was NOT processed, test date was processed is  NOT required"""
        self.data['process_rapid_test'] = NOT_APPLICABLE
        self.data['date_of_rapid_test'] = timezone.now().date()
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn(u'You indicated that a rapid test was NOT processed, yet rapid test date was provided. '
                      'Please correct.', form.errors.get('__all__'))

    def test_process_rapid_yes_result_req(self):
        """If rapid test was processed, test result was processed is required"""
        self.data['process_rapid_test'] = YES
        self.data['date_of_rapid_test'] = timezone.now().date()
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn(u'You indicated that a rapid test was processed. Please provide a result.',
                      form.errors.get('__all__'))

    def test_process_rapid_no_result_not_req(self):
        """If rapid test was NOT processed, test result was processed is NOT required"""
        self.data['process_rapid_test'] = NO
        self.data['rapid_test_result'] = POS
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn(u'You indicated that a rapid test was NOT processed, yet rapid test result was provided. '
                      'Please correct.', form.errors.get('__all__'))

    def test_process_rapid_na_result_not_req(self):
        """If rapid test was NOT processed, test result was processed is NOT required"""
        self.data['process_rapid_test'] = NOT_APPLICABLE
        self.data['rapid_test_result'] = NEG
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn(u'You indicated that a rapid test was NOT processed, yet rapid test result was provided. '
                      'Please correct.', form.errors.get('__all__'))

    def test_regimen_duration_na(self):
        self.data['valid_regimen'] = YES
        self.data['valid_regimen_duration'] = NOT_APPLICABLE
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn(u'You have indicated that the participant is on ARV. Regimen validity period'
                      ' CANNOT be Not Applicable. Please correct.', form.errors.get('__all__'))

    def test_regimen_duration_yes(self):
        self.data['valid_regimen'] = NO
        self.data['valid_regimen_duration'] = YES
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn(u'You have indicated that there are no records of Participant taking ARVs. '
                      'Regimen validity period should be Not Applicable. Please correct.', form.errors.get('__all__'))

    def test_regimen_duration_no(self):
        self.data['valid_regimen'] = NO
        self.data['valid_regimen_duration'] = NO
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn(u'You have indicated that there are no records of Participant taking ARVs. '
                      'Regimen validity period should be Not Applicable. Please correct.', form.errors.get('__all__'))

    def test_hiv_evidence_pos(self):
        self.data['evidence_hiv_status'] = NOT_APPLICABLE
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn(u'You have indicated that the participant is Positive, Evidence of HIV '
                      'result CANNOT be Not Applicable. Please correct.', form.errors.get('__all__'))

    def test_hiv_evidence_pos_reg_na(self):
        self.data['valid_regimen'] = NOT_APPLICABLE
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn(u'You have indicated that the participant is Positive, "do records show that'
                      ' participant takes ARVs" cannot be Not Applicable.', form.errors.get('__all__'))

    def test_hiv_evidence_neg(self):
        self.data['verbal_hiv_status'] = NEG
        self.data['evidence_hiv_status'] = NOT_APPLICABLE
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn(u'You have indicated that the participant is Negative, Evidence of HIV '
                      'result CANNOT be Not Applicable. Please correct.', form.errors.get('__all__'))

    def test_sample_filled_before_enrollment(self):
        sample_consent = SampleConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        if not sample_consent:
            # self.assertIn(u'Please ensure to save the SAMPLE CONSENT before completing Enrollment')
            self.assertRaises(forms.ValidationError)

    def test_pos_with_evidence_and_do_rapid_test(self):
        self.data['evidence_hiv_status'] = YES
        self.data['process_rapid_test'] = YES
        form = BaseEnrollTestForm(data=self.data)
        self.assertIn(u'DO NOT PROCESS RAPID TEST. PARTICIPANT IS POS and HAS EVIDENCE.', form.errors.get('__all__'))
