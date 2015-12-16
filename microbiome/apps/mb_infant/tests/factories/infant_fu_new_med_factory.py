import factory

from django.utils import timezone

from microbiome.apps.mb_infant.models import InfantFuNewMed

from edc_constants.constants import YES


class InfantFuNewMedFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantFuNewMed

    new_medications = YES
    report_datetime = timezone.now()
