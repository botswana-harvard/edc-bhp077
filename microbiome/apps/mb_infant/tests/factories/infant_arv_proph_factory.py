import factory

from edc_constants.constants import YES

from microbiome.apps.mb_infant.models import InfantArvProph, InfantArvProphMod
from microbiome.apps.mb_infant.choices import ARV_DRUG_LIST


class InfantArvProphFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantArvProph

    prophylatic_nvp = YES


class InfantArvProphModFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantArvProphMod

    infant_arv_proph = factory.SubFactory(InfantArvProphFactory)
    arv_code = ARV_DRUG_LIST[0][0]
