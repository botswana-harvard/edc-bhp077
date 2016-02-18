import factory

from microbiome.apps.mb_infant.models import InfantCardioDisorder

from .infant_congenital_anomalies_factory import InfantCongenitalAnomaliesFactory


class InfantCardioDisorderFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantCardioDisorder

    congenital_anomalies = factory.SubFactory(InfantCongenitalAnomaliesFactory)
    cardio_disorder = 'Mitral valve stenosis or atresia'
    abnormality_status = 'CONFIRMED'
