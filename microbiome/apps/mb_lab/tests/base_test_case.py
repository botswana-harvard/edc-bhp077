from django.test.testcases import TestCase

from microbiome.load_edc import load_edc


class BaseTestCase(TestCase):
    """Test eligibility of a mother for antenatal enrollment."""

    def setUp(self):
        load_edc()
        self.study_site = '40'
