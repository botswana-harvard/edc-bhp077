from django.test import TestCase

from ...maternal import AntenatalEnrollment


class GenerateCallListTests(TestCase):

    def test_generate_call_list(self):
        """Test create call log."""
        antenatal_enrollment = AntenatalEnrollmentFactory(weeks_of_gestation=32)
