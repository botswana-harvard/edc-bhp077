import factory

from django.utils import timezone

from edc_constants.constants import YES

from microbiome.apps.mb_infant.models import InfantFuNewMed


class InfantFuNewMedFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantFuNewMed

    new_medications = YES
    report_datetime = timezone.now()
