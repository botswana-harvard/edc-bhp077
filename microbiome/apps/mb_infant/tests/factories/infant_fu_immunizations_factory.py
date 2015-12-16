import factory

from django.utils import timezone

from microbiome.apps.mb_infant.models import InfantFuImmunizations

from edc_constants.constants import YES, NO


class InfantFuImmunizationsFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantFuImmunizations

    vaccines_received = YES
    vaccines_missed = NO
