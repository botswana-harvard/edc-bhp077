import factory

from django.utils import timezone

from bhp077.apps.microbiome_infant.models import InfantBirthFeedVaccine
from bhp077.apps.microbiome.constants import BREASTFEED_ONLY
from .infant_visit_factory import InfantVisitFactory


class InfantBirthFeedVaccineFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantBirthFeedVaccine

    infant_visit = factory.SubFactory(InfantVisitFactory)
    report_datetime = timezone.now()
    feeding_after_delivery = BREASTFEED_ONLY
