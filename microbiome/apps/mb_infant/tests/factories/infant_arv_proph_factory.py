import factory

from django.utils import timezone

from edc_constants.constants import YES

from microbiome.apps.mb_infant.models import InfantArvProph, InfantArvProphMod
from microbiome.apps.mb_infant.choices import ARV_DRUG_LIST

from ...choices import ARV_MODIFICATION_REASON, DOSE_STATUS


class InfantArvProphFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantArvProph

    prophylatic_nvp = YES


class InfantArvProphModFactory(factory.DjangoModelFactory):

    class Meta:
        model = InfantArvProphMod

    infant_arv_proph = factory.SubFactory(InfantArvProphFactory)
    arv_code = ARV_DRUG_LIST[0][0]
    dose_status = DOSE_STATUS[0][0]
    modification_date = timezone.now().date()
    modification_code = ARV_MODIFICATION_REASON[0][0]
