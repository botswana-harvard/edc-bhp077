import factory
from django.utils import timezone

from edc_constants.constants import YES, NO

from bhp077.apps.microbiome_maternal.models import SexualReproductiveHealth

from .maternal_visit_factory import MaternalVisitFactory


class SexualReproductiveHealthFactory(factory.DjangoModelFactory):

    class Meta:
        model = SexualReproductiveHealth

    report_datetime = timezone.now()
    maternal_visit = factory.SubFactory(MaternalVisitFactory)
    more_children = YES
    contraceptive_measure = YES
    uses_contraceptive = NO
    srh_referral = YES
