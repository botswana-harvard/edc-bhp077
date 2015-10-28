import factory

from django.utils import timezone
from edc_registration.tests.factories import RegisteredSubjectFactory
from edc_constants.constants import NOT_APPLICABLE, YES, NEG

from ...maternal.models import MaternalEligibility


class MaternalEligibilityFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalEligibility

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    report_datetime = timezone.now()
    disease = NOT_APPLICABLE
    currently_pregnant = YES
#     pregnancy_weeks = 37
    verbal_hiv_status = NEG
    rapid_test_result = NEG
    rapid_test_result_datetime = timezone.now()
