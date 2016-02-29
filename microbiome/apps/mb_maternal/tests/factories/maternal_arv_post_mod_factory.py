import factory

from django.utils import timezone

from microbiome.apps.mb_maternal.models import MaternalArvPostMod
from microbiome.apps.mb_maternal.tests.factories import MaternalArvPostFactory

from ...maternal_choices import ARV_DRUG_LIST, DOSE_STATUS, ARV_MODIFICATION_REASON


class MaternalArvPostModFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalArvPostMod

    maternal_arv_post = factory.SubFactory(MaternalArvPostFactory)
    arv_code = ARV_DRUG_LIST[0][0]
    dose_status = DOSE_STATUS[0][0]
    modification_date = timezone.now().date()
    modification_code = ARV_MODIFICATION_REASON[0][0]
