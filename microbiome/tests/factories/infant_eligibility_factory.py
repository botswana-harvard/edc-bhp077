import factory
from django.utils import timezone

from ...models import InfantEligibility
from ..factories import MaternalEligibilityPostFactory


class InfantEligibilityFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantEligibility

    maternal_enrollment_post = factory.SubFactory(MaternalEligibilityPostFactory)
    report_datetime = timezone.now()
    infant_hiv_result = 'POS'
