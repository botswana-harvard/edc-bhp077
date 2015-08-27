import factory
from django.utils import timezone
from edc_registration.tests.factories import RegisteredSubjectFactory

from ...models import MaternalEligibilityPost
from ...choices import NOT_APPLICABLE

class MaternalEligibilityPostFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalEligibilityPost

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    report_datetime = timezone.now()
    disease = NOT_APPLICABLE
    currently_pregnant = 'Yes'
#     pregnancy_weeks = 37
    verbal_hiv_status = 'NEG'
    rapid_test_result = 'NEG'
    rapid_test_result_datetime = timezone.now()
