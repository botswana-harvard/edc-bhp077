import factory
from django.utils import timezone
from edc_constants.constants import POS

from bhp077.apps.microbiome_infant.models import InfantEligibility

from bhp077.apps.microbiome_maternal.tests.factories.maternal_eligibility_factory import MaternalEligibilityFactory


class InfantEligibilityFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantEligibility

    maternal_enrollment_post = factory.SubFactory(MaternalEligibilityFactory)
    report_datetime = timezone.now()
    infant_hiv_result = POS
