import factory

from django.utils import timezone

from microbiome.apps.mb_lab.models import InfantRequisition
from microbiome.apps.mb_infant.tests.factories import InfantVisitFactory


class InfantRequistionFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantRequisition

    report_datetime = timezone.now()
    infant_visit = factory.SubFactory(InfantVisitFactory)
    requisition_datetime = timezone.now()
    drawn_datetime = timezone.now()
