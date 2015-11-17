import factory

from bhp077.apps.microbiome_list.models import Suppliments


class SupplimentsFactory(factory.DjangoModelFactory):

    name = 'Cotrimaxazole'
    short_name = 'CTX'
    display_index = 10
    version = '1.0'

    class Meta:
        model = Suppliments
