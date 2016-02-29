import factory

from edc_constants.constants import YES, NO

from microbiome.apps.mb_infant.models import InfantFuImmunizations, VaccinesMissed, VaccinesReceived

from ...choices import IMMUNIZATIONS


class InfantFuImmunizationsFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantFuImmunizations

    vaccines_received = YES
    vaccines_missed = NO


class VaccinesMissedFactory(factory.DjangoModelFactory):

    class Meta:
        model = VaccinesMissed

    infant_fu_immunizations = factory.SubFactory(InfantFuImmunizationsFactory)
    missed_vaccine_name = IMMUNIZATIONS[0][0]


class VaccinesReceivedFactory(factory.DjangoModelFactory):

    class Meta:
        model = VaccinesReceived

    infant_fu_immunizations = factory.SubFactory(InfantFuImmunizationsFactory)
    received_vaccine_name = IMMUNIZATIONS[0][0]

