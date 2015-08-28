import factory
from django.utils import timezone
from edc_constants.constants import POS

from ...models import InfantEligibility

from .maternal_eligibility_factory import MaternalEligibilityFactory


class InfantEligibilityFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantEligibility

    maternal_enrollment_post = factory.SubFactory(MaternalEligibilityFactory)
    report_datetime = timezone.now()
    infant_hiv_result = POS
