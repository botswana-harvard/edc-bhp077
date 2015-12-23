from edc_call_manager.caller_site import site_model_callers
from edc_call_manager.models import Call
from edc_constants.constants import POS, NO, YES, NOT_APPLICABLE

from microbiome.apps.mb_maternal.model_callers import AnteNatalModelCaller
from microbiome.apps.mb_maternal.models import AntenatalEnrollment
from microbiome.apps.mb_maternal.tests.factories.maternal_consent_factory import MaternalConsentFactory
from microbiome.apps.mb_maternal.tests.factories.maternal_eligibility_factory import MaternalEligibilityFactory

from .base_maternal_test_case import BaseMaternalTestCase
from .factories import AntenatalEnrollmentFactory


class TestModelCaller(BaseMaternalTestCase):

    def setUp(self):
        super(TestModelCaller, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.registered_subject = self.maternal_eligibility.registered_subject
        self.maternal_consent = MaternalConsentFactory(
            registered_subject=self.registered_subject,
            study_site=self.study_site)

    def test_model_caller_registers(self):
        self.assertIsInstance(
            site_model_callers._registry['scheduling_models'].get(AntenatalEnrollment), AnteNatalModelCaller)

    def test_schedules_call(self):
        antenatal_enrollment = AntenatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=POS,
            evidence_hiv_status=YES,
            rapid_test_done=NOT_APPLICABLE,
            on_hypertension_tx=NO)
        subject_identifier = antenatal_enrollment.get_subject_identifier()
        self.assertEqual(Call.objects.filter(subject_identifier=subject_identifier).count(), 1)
