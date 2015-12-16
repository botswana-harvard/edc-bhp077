import factory

from microbiome.apps.mb_list.models import Supplements, ChronicConditions
from microbiome.apps.mb_list.models.maternal_lab_del import HealthCond


class SupplementsFactory(factory.DjangoModelFactory):

    name = 'N/A'
    short_name = 'N/A'
    display_index = 10
    version = '1.0'

    class Meta:
        model = Supplements


class HealthCondFactory(factory.DjangoModelFactory):

    name = 'N/A'
    short_name = 'N/A'
    display_index = 20
    version = '1.0'

    class Meta:
        model = HealthCond


class ChronicConditionsFactory(factory.DjangoModelFactory):

    name = 'N/A'
    short_name = 'N/A'
    display_index = 20
    version = '1.0'

    class Meta:
        model = ChronicConditions
