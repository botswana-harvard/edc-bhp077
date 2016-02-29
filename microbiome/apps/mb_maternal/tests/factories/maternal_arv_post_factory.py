import factory

from edc_constants.constants import YES
from edc_constants.choices import ARV_STATUS_WITH_NEVER

from microbiome.apps.mb_maternal.models import MaternalArvPost

from ...maternal_choices import REASON_FOR_HAART


class MaternalArvPostFactory(factory.DjangoModelFactory):

    class Meta:
        model = MaternalArvPost

    on_arv_since = YES
    on_arv_reason = REASON_FOR_HAART[0][0]
    arv_status = ARV_STATUS_WITH_NEVER[0][0]
