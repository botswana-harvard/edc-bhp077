from edc_constants.constants import YES, NEG

from .base_maternal_test_case import BaseMaternalTestCase
from .factories import MaternalConsentFactory, MaternalEligibilityFactory, PostnatalEnrollmentFactory


class TestMaternalLocator(BaseMaternalTestCase):

    def setUp(self):
        super(TestMaternalLocator, self).setUp()
        self.maternal_eligibility = MaternalEligibilityFactory()
        self.maternal_consent = MaternalConsentFactory(registered_subject=self.maternal_eligibility.registered_subject)
        self.registered_subject = self.maternal_consent.registered_subject
        PostnatalEnrollmentFactory(
            registered_subject=self.registered_subject,
            current_hiv_status=NEG,
            evidence_hiv_status=YES,
            rapid_test_done=YES,
            rapid_test_result=NEG)

    def test_maternal_locator(self):
        pass
