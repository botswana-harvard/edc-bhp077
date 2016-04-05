import factory

from django.utils import timezone

from microbiome.apps.mb_infant.models import InfantOffStudy

from .infant_visit_factory import InfantVisitFactory


class InfantOffStudyFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantOffStudy

    offstudy_date = timezone.now().date()

    infant_visit = factory.SubFactory(InfantVisitFactory)
