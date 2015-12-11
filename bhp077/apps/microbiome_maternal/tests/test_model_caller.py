from django.test import TestCase

from edc.core.bhp_variables.tests.factories.study_site_factory import StudySiteFactory
from edc.lab.lab_profile.classes.controller import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes.controller import site_lab_tracker
from edc.subject.rule_groups.classes.controller import site_rule_groups
from edc_call_manager.caller_site import site_model_callers
from edc_call_manager.models import Call
from edc_constants.constants import POS, NO, YES, NOT_APPLICABLE

from bhp077.apps.microbiome.app_configuration.classes.microbiome_configuration import MicrobiomeConfiguration
from bhp077.apps.microbiome_lab.lab_profiles import MaternalProfile
from bhp077.apps.microbiome_maternal.model_callers import AnteNatalModelCaller
from bhp077.apps.microbiome_maternal.models import AntenatalEnrollment
from bhp077.apps.microbiome_maternal.tests.factories.maternal_consent_factory import MaternalConsentFactory
from bhp077.apps.microbiome_maternal.tests.factories.maternal_eligibility_factory import MaternalEligibilityFactory

from .factories import AntenatalEnrollmentFactory


class TestModelCaller(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(MaternalProfile())
        except AlreadyRegisteredLabProfile:
            pass
        MicrobiomeConfiguration().prepare()
        site_lab_tracker.autodiscover()
        site_rule_groups.autodiscover()
        self.study_site = StudySiteFactory(site_code='10', site_name='Gabs')
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
