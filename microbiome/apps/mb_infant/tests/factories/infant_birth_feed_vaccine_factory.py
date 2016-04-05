import factory

from django.utils import timezone

from microbiome.apps.mb_infant.models import InfantBirthFeedVaccine, InfantVaccines
from microbiome.apps.mb.constants import BREASTFEED_ONLY

from .infant_visit_factory import InfantVisitFactory

from ...choices import INFANT_VACCINATIONS


class InfantBirthFeedVaccineFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantBirthFeedVaccine

    infant_visit = factory.SubFactory(InfantVisitFactory)
    report_datetime = timezone.now()
    feeding_after_delivery = BREASTFEED_ONLY


class InfantVaccinesFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantVaccines

    infant_birth_feed_vaccine = factory.SubFactory(InfantBirthFeedVaccineFactory)
    vaccination = INFANT_VACCINATIONS[0][0]
