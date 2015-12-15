import factory

from django.utils import timezone

from microbiome.apps.mb_infant.models import InfantFu

from edc_constants.constants import YES


class InfantFuFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantFu

    report_datetime = timezone.now()
    physical_assessment = YES
    diarrhea_illness = YES
    has_dx = YES
    was_hospitalized = YES
    days_hospitalized = 2
