import factory

from bhp077.apps.microbiome_list.models import Suppliments
from bhp077.apps.microbiome_list.models.maternal_lab_del import HealthCond


class SupplimentsFactory(factory.DjangoModelFactory):

    name = 'N/A'
    short_name = 'N/A'
    display_index = 10
    version = '1.0'

    class Meta:
        model = Suppliments


class HealthCondFactory(factory.DjangoModelFactory):

    name = 'N/A'
    short_name = 'N/A'
    display_index = 20
    version = '1.0'

    class Meta:
        model = HealthCond
