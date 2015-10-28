from django.test import TestCase

from ...maternal.models import AntenatalEnrollment
from ...tests.factories import AntenatalEnrollmentFactory

from ..views import GenerateCallList
from ..models import AntenatalCallList


class TestGenerateCallList(TestCase):

    def test_generate_call_list(self):
        """Test create call log."""
        AntenatalEnrollmentFactory(weeks_of_gestation=32)
        GenerateCallList().create_antenatal_call_list()
        antenatal_enrollment = AntenatalEnrollment.objects.all().count()
        self.assertEqual(antenatal_enrollment, 1)
        self.assertEqual(AntenatalCallList.objects.all().count(), 1)
