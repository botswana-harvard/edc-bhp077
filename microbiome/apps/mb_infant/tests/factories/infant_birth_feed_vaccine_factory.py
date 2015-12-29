import factory

from django.utils import timezone

from microbiome.apps.mb_infant.models import InfantBirthFeedVaccine
from microbiome.apps.mb.constants import BREASTFEED_ONLY

from .infant_visit_factory import InfantVisitFactory


class InfantBirthFeedVaccineFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantBirthFeedVaccine

    infant_visit = factory.SubFactory(InfantVisitFactory)
    report_datetime = timezone.now()
    feeding_after_delivery = BREASTFEED_ONLY
