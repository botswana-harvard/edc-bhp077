import factory

from edc_constants.constants import YES, NO

from microbiome.apps.mb_maternal.models import MaternalArvPreg, MaternalArv

from ...maternal_choices import ARV_DRUG_LIST


class MaternalArvPregFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalArvPreg

    took_arv = YES
    is_interrupt = NO


class MaternalArvFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalArv

    maternal_arv_preg = factory.SubFactory(MaternalArvPregFactory)
    arv_code = ARV_DRUG_LIST[0][0]
