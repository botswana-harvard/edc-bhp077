import factory

from django.utils import timezone

from bhp077.apps.microbiome_lab.models import InfantRequisition
from bhp077.apps.microbiome_infant.tests.factories import InfantVisitFactory


class InfantRequistionFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantRequisition

    report_datetime = timezone.now()
    infant_visit = factory.SubFactory(InfantVisitFactory)
