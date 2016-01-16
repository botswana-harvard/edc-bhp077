from django.test.testcases import TestCase

from microbiome.load_edc import load_edc


class BaseTestCase(TestCase):

    def setUp(self):
        load_edc()
