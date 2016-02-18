import factory

from microbiome.apps.mb_infant.models import InfantCleftDisorder

from .infant_congenital_anomalies_factory import InfantCongenitalAnomaliesFactory


class InfantCleftDisorderFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantCleftDisorder

    congenital_anomalies = factory.SubFactory(InfantCongenitalAnomaliesFactory)
    cleft_disorder = 'Cleft palate without cleft lip'
    abnormality_status = 'CONFIRMED'
