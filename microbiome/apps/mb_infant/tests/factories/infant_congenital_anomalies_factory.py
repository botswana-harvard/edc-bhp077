import factory

from microbiome.apps.mb_infant.models import InfantCongenitalAnomalies

from .infant_visit_factory import InfantVisitFactory


class InfantCongenitalAnomaliesFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantCongenitalAnomalies

    infant_visit = factory.SubFactory(InfantVisitFactory)
