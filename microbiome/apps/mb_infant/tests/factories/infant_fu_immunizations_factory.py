import factory

from edc_constants.constants import YES, NO

from microbiome.apps.mb_infant.models import InfantFuImmunizations


class InfantFuImmunizationsFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantFuImmunizations

    vaccines_received = YES
    vaccines_missed = NO
