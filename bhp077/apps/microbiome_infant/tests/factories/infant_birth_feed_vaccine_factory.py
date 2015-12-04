import factory

from django.utils import timezone

from bhp077.apps.microbiome_infant.models import InfantBirthFeedVaccine

from .infant_visit_factory import InfantVisitFactory
from .infant_birth_factory import InfantBirthFactory


class InfantBirthFeedVaccineFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantBirthFeedVaccine

    infant_visit = factory.SubFactory(InfantVisitFactory)
    report_datetime = timezone.now()
    feeding_after_delivery = 'Breastfeeding only'
