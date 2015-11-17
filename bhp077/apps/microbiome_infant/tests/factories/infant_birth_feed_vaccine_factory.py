import factory

from django.utils import timezone

from bhp077.apps.microbiome_infant.models import InfantBirthFeedVaccine

from bhp077.apps.microbiome_infant.tests.factories import InfantBirthFactory


class InfantBirthFeedVaccineFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantBirthFeedVaccine

    report_datetime = timezone.now()

    infant_birth = factory.SubFactory(InfantBirthFactory)

    feeding_after_delivery = 'Breastfeeding only'
