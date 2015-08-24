import factory
from django.utils import timezone
from edc_registration.tests.factories import RegisteredSubjectFactory

from ...models import MaternalEligibilityPost


class MaternalEligibilityPostFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalEligibilityPost

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    report_datetime = timezone.now()
    days_post_natal = 2
    weeks_of_gestation = 37
    type_of_birth = 'vaginal'
    live_infants = 2
