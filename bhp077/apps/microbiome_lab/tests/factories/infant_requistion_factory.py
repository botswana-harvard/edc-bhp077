import factory

from django.utils import timezone
from edc_constants.constants import ALIVE

from bhp077.apps.microbiome_lab.models import InfantRequisition
from bhp077.apps.microbiome_infant


class InfantRequistionFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantRequisition

    report_datetime = timezone.now()
    infant_visit = factory.SubFactory(InfantVisitFactory)
