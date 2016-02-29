import factory

from django.utils import timezone

from edc_constants.constants import YES
from edc_constants.choices import DRUG_ROUTE

from microbiome.apps.mb_infant.models import InfantFuNewMed, InfantFuNewMedItems
from microbiome.apps.mb.choices import MEDICATIONS


class InfantFuNewMedFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantFuNewMed

    new_medications = YES
    report_datetime = timezone.now()


class InfantFuNewMedItemsFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantFuNewMedItems

    infant_fu_med = factory.SubFactory(InfantFuNewMedFactory)
    medication = MEDICATIONS[0][0]
    date_first_medication = timezone.now().date()
    drug_route = DRUG_ROUTE[0][0]
